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


## The pixelID given by Rick's electronics is a unique ID for pixels in the
## detector system. It is different from what we usually call a pixelID, which
## is the ID of a pixel in a detector tube (0-128 or 256).
## Here, we call Rick's pixelID
## "longpixelID", and implement a method to calculate longpixelID from
## packID, tubeID, and pixelID.


class PixelIDMapper(object):


    def __init__(self, nPixelsPerDetector, nDetectorsPerPack, nPacks ):
        nPixelsPerPack = nDetectorsPerPack * nPixelsPerDetector
        
        assert nPixelsPerPack%1024==0
        assert nDetectorsPerPack==8
        
        # number of bits to shift
        from math import log
        self.nbits_pack = int( log( nPixelsPerPack, 2 ) )
        self.nbits_det = int( log( nPixelsPerDetector, 2 ) )
        self.ntotpixels = (nPacks) << self.nbits_pack
        return


    def longpixelID(self, packID, tubeID, pixelID ):
        # need to subtract 1 from packID because in ARCS packID starts from 1
        ret = pixelID + (tubeID << self.nbits_det) + ( (packID-1) << self.nbits_pack )
        return ret

    pass # end of PixelIDMapper


# version
__id__ = "$Id$"

#  End of file 
