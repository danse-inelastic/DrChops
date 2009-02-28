#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction import units
meter = units.length.meter
cm = units.length.cm


'''calculate solid angles of pixels for ARCS instrument

For ARCS, all tubes are vertical. The solid angle is

    pixelarea * cos(theta) / r**2

where r is the distance from sample to pixel, pixelarea is the area
of a pixel (2*radius*height), and theta is the angle between kf and
the horizontal plane.
'''


def solidangles(pixelpositions, arcs,
                nPixelsPerDetector, nDetectorsPerPack, nPacks):
    packs = _getPacks(arcs, nPixelsPerDetector, nDetectorsPerPack, nPacks)
    return solidangles1(
        pixelpositions, packs,
        npixelspertube=nPixelsPerDetector,
        ntubesperpack=nDetectorsPerPack)



def _getPacks(arcs,
              nPixelsPerDetector, nDetectorsPerPack, nPacks ):

    nPixelsPerPack = nPixelsPerDetector * nDetectorsPerPack
    
    from longpixelID import PixelIDMapper
    ids2longpixelID = PixelIDMapper( nPixelsPerDetector, nDetectorsPerPack, nPacks )
    ntotpixels = ids2longpixelID.ntotpixels
    
    # array to hold results
    res = [None for i in range(nPacks)]

    from instrument.elements.DetectorVisitor import DetectorVisitor
    class _( DetectorVisitor ):
        def onDetectorPack(self, pack):
            detindexes = self.detectorElementSignature()

            packID, = detindexes
            
            longpixelID = ids2longpixelID.longpixelID( packID, 0, 0 )
            packindex = longpixelID/nPixelsPerPack

            tube = pack.elements()[0]
            cyl = tube.shape()
            length = cyl.height/meter
            radius = cyl.radius/meter
            
            p = Pack()
            p.length = length; p.radius = radius
            res[packindex] = p
            return
    _().render(arcs, arcs.geometer)
    return res


class Pack:
    length = None # length of tubes in this pack
    radius = None # radius of tubes in this pack

def solidangles1(pixelpositions, packs,
                npixelspertube=128, ntubesperpack=8):
    '''calculate solid angles for some detector packs

  assumptions:
    * all packs have same number of tubes
    * all tubes have same number of pixels
    * all tubes vertical
  
  pixelpositions: a numpy array of positions of pixels of all packs
  packs: an array of instances of Pack.
  '''
    save = pixelpositions.shape
    pixelpositions.shape = -1, 3
    x = pixelpositions[:,0]; y = pixelpositions[:,1]; z = pixelpositions[:,2]
    pixelpositions.shape = save

    npixels = len(x)

    import numpy
    r = numpy.zeros(npixels, 'd')
    h = numpy.zeros(npixels, 'd')
    npixelsperpack = npixelspertube * ntubesperpack
    
    for i, pack in enumerate(packs):
        r[i*npixelsperpack:(i+1)*npixelsperpack] = pack.radius
        h[i*npixelsperpack:(i+1)*npixelsperpack] = pack.length/npixelspertube
        continue

    return solidangle2(x,y,z,r,h)


def solidangle2(x,y,z,r,h):
    '''solid angle of a pixel at position(x,y,z)
    tube is assumed to be vertical.
    r: radius of tube
    h: height of pixel
    '''
    r2 = x*x + y*y + z*z
    cost = (1 - z*z/r2)**0.5
    area = 2*r*h*cost
    return solidangle1(area, r2)


def solidangle1(area, radius_square):
    '''basic formula to calculate solid angle
    sa = area/radius**2
    '''
    return area/radius_square



# version
__id__ = "$Id$"

# End of file 
