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


## This script reads events from event data file
## and create a histogram hdf5 file of I(dspacing)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        dspacingparams = Tuple( 't', default = '0,5,0.01' )
        dspacingparams.meta['tip'] = "d-spacing bin parameters (begin, end, step). units: angstrom"

        ARCSxml = pinv.str('x', default = "ARCSxml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        dspacingparams = self.inventory.dspacingparams
        return ARCSxml, dspacingparams


    def _defaults(self):
        base._defaults(self)
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


from arcseventdata.pyre_support.AbstractHistogrammer import AbstractHistogrammer
class Engine(AbstractHistogrammer):
    
    def _run(self, eventdatafilename, start, nevents,
             ARCSxml, dspacingparams ):
        
        self._info.log( "nevents = %s" % nevents )
        
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
        self._info.log( "pixel-positions-filename=%s" % pixelPositionsFilename )
        
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

    pass # end of Engine



def main():
    Application('idspacing').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer1' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
