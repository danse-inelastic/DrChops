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

    from longpixelID import PixelIDMapper
    ids2longpixelID = PixelIDMapper( nPixelsPerDetector, nDetectorsPerPack, nPacks )
    ntotpixels = ids2longpixelID.ntotpixels
    
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
            
            longpixelID = ids2longpixelID.longpixelID( packID, detID, pixelID )

            res[longpixelID] = position/meter

            #print detindexes, longpixelID, res[longpixelID]
            
            return

        pass # end of Mapper

    Mapper().render( arcs, arcs.geometer )

    return res



# version
__id__ = "$Id$"

#  End of file 
