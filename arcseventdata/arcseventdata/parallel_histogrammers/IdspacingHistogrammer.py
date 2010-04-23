#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import arcseventdata, histogram 

from ParallelHistogrammer import ParallelHistogrammer as base, info

class IdspacingHistogrammer(base):
    
    def setParameters(
        self, 
        ARCSxml, dspacingparams ):
        
        infos = self._readInstrumentInfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
        
        info.log( "pixel-positions-filename=%s" % pixelPositionsFilename )
        
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet )

        from arcseventdata.longpixelID import PixelIDMapper
        m = PixelIDMapper( npixelsperdet, ndetsperpack, npacks )
        assert m.ntotpixels == len( pixelPositions )
        
        self.out_histogram = None

        self.pixelPositions = pixelPositions
        self.dspacingparams = dspacingparams
        self.mod2sample = mod2sample
        return


    def _processEvents(self, events):
        h = self.out_histogram = arcseventdata.e2Id(
            events.ptr, events.n, self.pixelPositions,
            self.dspacingparams,
            Idspacing = self.out_histogram,
            mod2sample = self.mod2sample)
        return h




# version
__id__ = "$Id$"

# End of file 
