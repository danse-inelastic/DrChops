#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def createmap( arcs, nPixelsPerDetector, nDetectorsPerPack, nPacks ):

    nPixelsPerPack = nDetectorsPerPack * nPixelsPerDetector

    assert nPixelsPerPack%1024==0
    assert nDetectorsPerPack==8

    # number of bits to shift
    from math import log
    nbits_pack = int( log( nPixelsPerPack, 2 ) )
    nbits_det = int( log( nPixelsPerDetector, 2 ) )
    ntotpixels = (nPacks+1) << nbits_pack

    # array to hold results
    import numpy
    res = numpy.zeros( ntotpixels * 3, 'd' )
    res.shape = ntotpixels, 3


    from pyre.units.length import meter
    
    from instrument.elements.DetectorVisitor import DetectorVisitor

    class Mapper( DetectorVisitor ):

        onDetector = DetectorVisitor.onElementContainer

        def onPixel(self, pixel):
            indexes = self.elementSignature(  )

            position = self._geometer.positionRelativeToSample( indexes )

            detindexes = self.detectorElementSignature()

            packID, detID, pixelID = detindexes
            
            longpixelID = pixelID + (detID << nbits_det) + ( (packID-1) << nbits_pack )

            res[longpixelID] = position/meter

            #print detindexes, longpixelID, res[longpixelID]
            
            return

        pass # end of Mapper

    Mapper().render( arcs, arcs.geometer )

    return res



# version
__id__ = "$Id$"

#  End of file 
