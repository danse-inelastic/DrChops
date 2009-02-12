#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.histCompat.Rebinner
## generic rebinner
##
## this is still in prototyping stage


import journal
warning = journal.warning( 'Rebinner' )
debug = journal.debug( 'Rebinner' )


class Rebinner( object):

    """Rebinner that converts one histogram to another

    Example 1:

      I(tof) --> I(E)

      can be done by rebinner.rebin( ItofHist, mapper, IEHist)

      here mapper is a function that has an interface: mapper( tof ) --> E

    Example 2:

      I(x,y) --> I(r)

    Example 3:

      I(tube, pixel, tof) -> I(phi, E)


    --------
    
    The algorithm implemented here works like this, by
    using a 2D example.
        
      1. calculate the coordinates of each cell center
         in the target (output) axes,
         So now we have a list of (u,v).
         Let us call this list InputUVList.
         
      2. A conversion always involvs Jacobians. The reason
      is, say we have a density function

        f(x,y)

      in the original histogram, and another density functino

        g(u,v)

      in the target histogram. Then we know that

        f(x,y) dxdy = g(u,v) dudv

      But we know that

        dudv = J dxdy

      So we have

        g(u,v) = f(x,y) / J

      Given the value of f(x,y) and J(x,y), we can calculate
      values of g(u,v) at each point (u,v) in the InputUVList
      obtained from step 1.
      
      3. Now in the (U,V) space, we have the output histogram
      which is defined on an evenly spaced grid. For each point
      on taht grid, we can compute the value of the histogram,
      g(u,v) du dv in the following way (Note, dudv here is
      the step size of the axes of the output histogram):

      For each point (u0, v0), search in the InputUVList, find
      thos points that are nearest neighbors of (u0, v0). Let us
      call that list NNList. For each poiint in the NNLIst, the
      value g(u,v) has been calculated in step 2, and it is an
      approximation of the value g(u0, v0) we are looking for.
      All we need to do is to make a reasonable average.
      
    """

    
    def rebin( self, inHist, outHist, mapper, Jacobians, SampleCellRelativeSize_UpperLimit=1.5, InversedJacobains = False, SampleCellRelativeSize_LowerLimit = 0.5, epsilon = 1e-5):
        """
        inHist: input histogram. A histogram is a way to represent
          a density function. For a histogram, the value at 
          a cell  (x,y) -- (x+dx, y+dy) is meant to be the product
          of the density function and the volume of the cell:

            f(x,y) * (dx * dy)

        outHist: output histogram

        mapper: the mapper function that maps the coordinates
          at the input histogram to the coordinates at the
          output histogram.
          
        Jacobians:

            J = det( (du/dx, ...), ..., (..., dv/dy) )

        InversedJacobains: Sometimes it would be optimal to
          have inversed Jacobians instead of Jacobains to avoid
          singularities. Set this to True, if you input the inversed
          Jacobians.

        SampleCellRelativeSize_UpperLimit: we don't want to waste
          too much time looking for neighbors. This parameter limit
          the size of the box around the point of interested.

        SampleCellRelativeSize_LowerLimit: we don't want to throw
          away some points of equal importance. All points inside
          the box defined by this parameter will be used for averaging
          computation.

        epsilon: if a point is really really close to the intereste
          of point, we are very lucky. That means we should not
          waste our time looking for other points. Just stop here.
        """
          

        axes = [ inHist.axisFromName( name ) for name in inHist.axisNameList() ]
        dim = len(axes)
        axisBinCentersList = [ axis.binCenters() for axis in axes ]

        #create a matrix of coordinates of cells for the input histogram
        from histogram import meshgrid
        Xmesh = meshgrid( *axisBinCentersList )
        Xmesh = [item.flatten() for item in Xmesh]
        Xmesh = numpy.array(Xmesh)
        Xmesh = Xmesh.transpose()

        # apply mapper to get the coordinates of each cell
        # in the output phase space
        inYList = [ (mapper( X ), inHist[X], Jacobians[X]) for X in Xmesh ]
        debug.log( "list of coordinates in output axes for all points in the input histogram: %s" % inYList )


        Yaxes = [ outHist.axisFromName( name ) for name in outHist.axisNameList() ]

        #bin sizes. assuming evenly spaced axes
        YbinSizes = numpy.array( [
            (axis.binCenters()[1]-axis.binCenters()[0]) \
            for axis in Yaxes ] )
        volumeRatio = cellVolume(Yaxes)/cellVolume(axes)

        #pls c.f. function findNeighbors
        DY = YbinSizes * SampleCellRelativeSize_UpperLimit
        DY2 = YbinSizes * SampleCellRelativeSize_LowerLimit
        DY3 = YbinSizes * epsilon
        nNeighbors = dim * 2

        if InversedJacobains:
            weightedAverage = weightedAverage_useInversedJacobians
        else:
            weightedAverage = weightedAverage_useNormalJacobians
            pass

        #loop over all cells in the output histogram
        #and compute 
        outHistShape = outHist.shape()
        indexes = [ 0 for i in range(len(outHistShape)) ]

        count = 0
        v = volume(outHist.shape())
        Yaxes = [axis.binCenters() for axis in Yaxes]
        while count < v:
            Y = [ axis[ i ] for i, axis in zip( indexes, Yaxes ) ]
            debug.log("loop to point in output histogram: %s" % (Y,) )
            neighbors = findNeighbors( Y, inYList, DY, DY2, DY3, nNeighbors)
            outHist[ Y ] = (
                weightedAverage( neighbors ) * volumeRatio).asTuple()
            increment( indexes, outHistShape )
            count += 1
            continue
        return

    pass # end of Rebinner


def weightedAverage_useNormalJacobians( neighbors ):
    #debug.log( 'neighbors= %s' %( neighbors, ) )
    I = pqvalue( 0. )
    n = pqvalue( 0. )
    for position, distance, intensity, Jacobian in neighbors:
        if distance == 0.0: return intensity/Jacobian
        weight = 1./distance
        I += weight * intensity
        n += weight * Jacobian
        continue
    if n == 0 or n == 0.:
        if I != 0 and I != 0.0:
            raise "I/n: %s/%s" % (I,n)
    try:
        return I/n
    except ZeroDivisionError:
        return pqvalue(0.0)



def cellVolume( axes ):
    binSizes = numpy.array( [
        (axis.binCenters()[1]-axis.binCenters()[0]) \
        for axis in axes ] )
    return volume( binSizes )
    

def weightedAverage_useInversedJacobians( neighbors ):
    #print neighbors
    I = pqvalue( 0. )
    n = pqvalue( 0. )
    for position, distance, intensity, Jacobian in neighbors:
        if distance == 0.0: return intensity*Jacobian
        weight = 1./distance
        I += weight * intensity * Jacobian
        n += weight 
        continue
    if n == 0 or n == 0.:
        if I != 0 and I != 0.0:
            raise "I/n: %s/%s" % (I,n)
    return I/n


def findNeighbors( Y, inYList, DY, DY2, DY3, nNeighbors):
    """find neighbors of point 'Y' in the given list
    of points.

    Y: coordinate of the point whose neighbors are to be found
    inYList: a list of points and associated properties
      (coordinates, intensity, Jacobian)
    DY: distance from any neighbor to the target point must be
      smaller than DY
    DY2: it is possible that there are a lot of points that
      are very close to the point that we are interested in. It
      is better to include them all, even if the number of
      neighbors has excceed nNeighbors.
    DY3: it is possible that we are extremely lucky that there
      is a point that is extremely close to the point of interest.
      We may simply take that point.
    nNeighbors: maximum number of neighbors
    """
    candidates = []
    nns = []
    for inY, intensity, Jacobian in inYList:
        
        outofbox = False
        for y, iny, dy in zip(Y, inY, DY):
            if abs(iny-y)>dy: outofbox = True; break
            continue
        if outofbox: continue

        distance = calcDistance( Y, inY, DY )
        record = [inY, distance, pqvalue(intensity), pqvalue(Jacobian) ]


        # find out if we find the lucky point
        lucky = True
        for y, iny, dy3 in zip(Y, inY, DY3):
            if abs(iny-y)>dy3: lucky = False; break
            continue
        if lucky: return [record]

        # find out if the point belongs to "nearest neighbors"
        outofbox = False
        for y, iny, dy2 in zip(Y, inY, DY2):
            if abs(iny-y)>dy2: outofbox = True; break
            continue
        if not outofbox : # nn
            nns.append( record )
        else: # not nn
            candidates.append( record )
        continue

    nExtra = nNeighbors - len( nns )
    #debug.log( "Number of nearest neighbors: %s" %  len(nns) )
    if nExtra <= 0: return nns # there is enough neighbors in nearest neighbors list
    
    return nns + sortByDistance( candidates, nExtra )


def _compDistance( x, y ):
    d = x[1]-y[1]
    if d > 0: return 1
    elif d < 0: return -1
    return 0

def sortByDistance( candidates, N ):
    """sort candidates by distance to the given point.
    At most N points can be returned.
    """
    candidates.sort( _compDistance )
    return candidates[ : N ]



def calcDistance( x, y, norm ):
    """ calculate 'normalized' distance between two points
    \sum [(xi-yi)/norm_i]**2
    """
    displacement = numpy.array(x) - y
    displacement/= norm
    return numpy.sqrt(numpy.dot(displacement, displacement))


def createJacobian( inAxes, outAxes, mapper ):
    """calculate the Jacobian of the cell in the 'output' phase
    space defined by the outAxes. The cell corresponds to
    a cell of the input histogram in the input phase space.
    """
    return



def increment( indexes, limits ):
    """increase indexes up to limits
    increment( [1,4,3], [3,10,8] ) --> indexes becomes [2,4,3]
    increment( [2,4,3], [3,10,8] ) --> indexes becomes [0,5,3]
    """
    for i, index in enumerate(indexes):
        if index < limits[i]-1:
            indexes[i] += 1
            break
        else :
            indexes[i] = 0


def volume(shape):
    from operator import mul
    return reduce(mul, shape)

import numpy
from histogram import pqvalue

rebinner = Rebinner()

# version
__id__ = "$Id: Rebinner.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
