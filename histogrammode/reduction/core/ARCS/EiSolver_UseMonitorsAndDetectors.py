#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


'''
solve inciindent energy by taking into account
 - monitors (some time one, some time two)
 - detectors

'''


'''
implementation

Assumptions:
 - 8-packs are separated to 3 rows
 - each row, centers of all packs have the exact same distances to sample position
   (eacept two packs near forward beam. they should be removed from this computation)
 - all packs are vertical
 - all packs are oriented so that their normals pointing (horizontally) to the
   z axis (the axis with origin at sample position and pointing upward vertically)

Simplification resulted from assuptions:
 - For the purpose of calculating incident energy, a pixel is unique only
   if its distance-to-sample is unique. So, for each 8-pack, only 4 detectors
   are unique. for each row, only one 8-pack is unique.
   Therefore, there are 4*128*3 unique pixels

Several histograms are introduced

 - irtpt: I(row, unique tube, pixel, tof)
 - ipt: I(unique pixel, tof)
 
'''

bottompacks_idrange = 1,38
middlepacks_idrange = 39,77
toppacks_idrange = 78,115

nrows = 3
npixelspertube = 128
nuniquetubes = 8/2


def solveEi( ipdpt, mitofs, eiguess, mdists = None, ARCSxml = 'ARCS.xml'):
    tvsd = getTvsD( ipdpt, mitofs, eiguess, mdists = mdists, ARCSxml = ARCSxml)
    from reduction.histCompat.PolynomialFitter import PolynomialFitter
    emission_time, reversed_velocity = PolynomialFitter(1).fit( tvsd )
    velocity = 1./reversed_velocity
    print velocity, emission_time
    return


def getTvsD( ipdpt, mitofs, eiguess,  mdists = None, ARCSxml = 'ARCS.xml' ):

    ipt = getipt( ipdpt )
    pixeltofs = getTofCenters_UniquePixels( ipt )

    import arcseventdata as aed
    ii = aed.getinstrumentinfo(ARCSxml)
    dists_hist = ii[ 'dists' ]
    pixeldists = getDistances_UniquePixels( dists_hist )
        
    pixeltofs, pixeldists = removeBadPoints_TofCentersAndDistance_Pixels( pixeltofs, pixeldists )

    # distances and tof centers for monitors
    from reduction import units

    if mdists is None:
        from arcseventdata import getinstrumentinfo
        mdists = [
            ii[ 'moderator-monitor1 distance' ] * units.length.meter,
            ii[ 'moderator-monitor2 distance' ] * units.length.meter,
            ]

    from reduction.utils import conversion as C
    velocity_guess = C.e2v( eiguess ) * units.length.meter / units.time.second
    mtofs, mdists = getTofCentersAndDistances_Monitors( mitofs, mdists, velocity_guess )

    mod2sample = ii['moderator-sample distance']

    dists = list(pixeldists + mod2sample) + list(mdists) 
    centers = list(pixeltofs) + list( mtofs )

    #import pickle
    #pickle.dump( (pixeldists, pixeltofs, mdists, mtofs, dists, centers),
    #                open('tmp.pkl','w') )

    centers, dists = sortTofCentersAndDistance_Pixels( centers, dists )
        
    import histogram as H
    h = H.histogram( 'tof', [ ('distance', dists, 'meter') ],
                     data = centers, unit = 'second' )
    
    #from histogram.plotter import defaultPlotter
    #defaultPlotter.plot( h )
    #pickle.dump( h, open('tvsd.pkl', 'w'))
    return h


def getirtpt( ipdpt ):
    'obtain histogram of I(row, tube(unique), pixel, tof)'
    bottom =ipdpt[ bottompacks_idrange, (), (), () ]
    middle =ipdpt[ middlepacks_idrange, (), (), () ]
    top =ipdpt[ toppacks_idrange, (), (), () ]

    all = [ top, middle, bottom ]

    summed_over_packs = [ h.sum('detectorpackID') for h in all ]

    irtpt = H.histogram(
        'irtpt',
        [
        ('rowID', range(nrows)),
        ('pairID', range(nuniquetubes)),
        ipdpt.axisFromName( 'pixelID' ),
        ipdpt.axisFromName('tof'),
        ]
        )

    tubepairs = [ (i, 7-i) for i in range(nuniquetubes) ]
    
    for row, h in enumerate( summed_over_packs ):
        for pairid, pair in enumerate( tubepairs ):
            tube1, tube2 = pair
            irtpt[ row, pairid, (), () ] = h[ tube1, (), () ] + h[ tube2, (), () ]
            continue
        continue

    return irtpt


def getipt( ipdpt ):
    'obtain I( unique pixel, tof )'
    irtpt = getirtpt( ipdpt )
    ipt = H.histogram(
        'ipt',
        [
        ('unique pixel ID', range( nrows * nuniquetubes * npixelspertube ) ),
        ipdpt.axisFromName( 'tof' ),
        ]
        )
    
    for row in range( nrows ):
        for t in range(nuniquetubes):
            for p in range(npixelspertube):
                ipt[ p + npixelspertube*( t + nuniquetubes * row ) , () ] = irtpt[ row, t, p, () ]
                continue
            continue
        continue
    return ipt


def getTofCenters_UniquePixels( ipt, minIntensity = 1. ):
    '''obtain centers (elastic peak position) of for each I(tof) curve in ipt

    return: *** must return values in seconds ***
    '''
    centers = []
    for p in ipt.axisFromId(1).binCenters():
        curve = ipt[ p, () ]
        # if curve does not have good statistics,
        # ignore (by setting center to zero)
        if curve.I.max() < minIntensity : centers.append( 0 )
        # else, log the peak position
        else: centers.append( findPeakPosition( curve, 2 ) )
        continue
    return centers



def getDistances_UniquePixels( dists_hist ):
    '''obtain distances to sample from "unique pixels"

    return: *** must return values in meters ***
    '''
    bottompackdists = pack1dists = dists_hist[1, (), ()]
    middlepackdists = pack45dists = dists_hist[45, (), ()]
    toppackdists = pack90dists = dists_hist[90, (), ()]

    dists = H.histogram(
        'dists',
        [
        ('rowID', range(nrows)),
        ('pairID', range(nuniquetubes)),
        ('pixelID', range(npixelspertube)),
        ]
        )

    dists[ 0, (), () ] = toppackdists[ (0,3), () ]
    dists[ 1, (), () ] = middlepackdists[ (0,3), () ]
    dists[ 2, (), () ] = bottompackdists[ (0,3), () ]

    ret = dists.I
    ret.shape = -1,

    return ret



def sortTofCentersAndDistance_Pixels( centers, dists ):
    '''sort tofcenters, distances so that we can later create a histogram
    '''
    dists = N.array(dists)
    centers = N.array(centers)

    indsort = dists.argsort()
    dists = dists[ indsort ]
    centers = centers[ indsort ]
    return centers, dists


def removeBadPoints_TofCentersAndDistance_Pixels( centers, dists ):
    '''remove strange points.
    The input should be tof centers and distances in units of
    seconds and meters. They should be only for pixels. Do not include
    those valeus for monitors here!!!
    '''
    median = N.median( centers )
    centers = N.array( centers )
    dists = N.array( dists )

    #only keep the "good points".
    #for ARCS, all pixels have very similar distances to
    #sample position. so the valid tof centers are
    #in a small range. The following code remove all points
    #that is outside of that range.
    
    goodpnts = (centers > median*0.94) * (centers < median*1.06)
    dists = dists[ goodpnts ]
    centers = centers[ goodpnts ]
    return centers, dists
#return H.histogram( 'h', [ ('x', dists, 'meter') ], data = centers, unit = 'second' )



def getTofCentersAndDistances_Monitors( itofs, dists, velocity_guess ):
    '''
    itofs is a list of I(tof) histogram for monitors
    dists is a list of distances (distance from monitor to sample)

    ** All inputs must have units attached
    ** All outputs will be  unitless. tof: second. dist: meter
    '''

    import reduction.units as units
    second = units.time.second
    meter = units.length.meter
    
    def _( dist, v ):
        t = dist/v 
        return t, t/10

    centers = []
    
    for itof, dist in zip( itofs, dists):
        
        tofunit = itof.axisFromName('tof').unit()
        t, w = _( dist, velocity_guess )
        t /= tofunit; w /= tofunit

        pk = itof[ (t-w, t+w) ]
        
        position = findPeakPosition( pk )

        centers.append( position * tofunit / second )

        continue

    dists = [ dist/meter for dist in dists ]
    
    return centers, dists

    

import arcseventdata as aed

import histogram as H
import numpy as N
from reduction.histCompat import findPeakPosition


# version
__id__ = "$Id$"

# End of file 
