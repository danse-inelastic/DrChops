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


from ParallelHistogrammer import ParallelHistogrammer as base, info

class IdspacingHistogrammer(base):
    
    def _run(self, eventdatafilename, start, nevents,
             ARCSxml, dspacingparams ):
        
        info.log( "nevents = %s" % nevents )
        
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
        
        info.log( "pixel-positions-filename=%s" % pixelPositionsFilename )
        
        import arcseventdata, histogram 
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet )

        from arcseventdata.longpixelID import PixelIDMapper
        m = PixelIDMapper( npixelsperdet, ndetsperpack, npacks )
        assert m.ntotpixels == len( pixelPositions )
        
        h = arcseventdata.e2Id(
            events, nevents, pixelPositions, dspacingparams,
            mod2sample = mod2sample )
        
        return h




# version
__id__ = "$Id$"

# End of file 
