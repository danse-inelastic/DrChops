#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                        (C) 2007-2009  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def getpixelsizes(arcs, npacks, ntubesperpack, npixelspertube):
    'return radii and heights of all pixels'
    ntotpixels = npacks*ntubesperpack*npixelspertube
    packs = _getPacks(
        arcs,
        npixelspertube, ntubesperpack, npacks)
    return _pixel_sizes(
        packs, 
        npixelspertube=npixelspertube,
        ntubesperpack=ntubesperpack)


# implementation deails
class Pack:
    length = None # length of tubes in this pack
    radius = None # radius of tubes in this pack

def _getPacks(arcs,
              nPixelsPerDetector, nDetectorsPerPack, nPacks ):
    # obtain information about packs
    # returned are a list of instances of class Pack

    from reduction import units
    meter = units.length.meter

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


def _pixel_sizes(packs,
                 npixelspertube=128, ntubesperpack=8):
    '''
    packs: instances of class Pack
    '''
    npacks = len(packs)
    
    import numpy
    shape = npacks, ntubesperpack, npixelspertube
    r = numpy.zeros(shape, 'd')
    h = numpy.zeros(shape, 'd')
    
    for i, pack in enumerate(packs):
        r[i, :, :] = pack.radius
        h[i, :, :] = pack.length/npixelspertube
        continue

    return r,h



# version
__id__ = "$Id$"

#  End of file 
