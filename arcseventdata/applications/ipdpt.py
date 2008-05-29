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
## and create a histogram hdf5 file of I(pack, detector, pixel, E)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        tof_params = Tuple( 't', default = '0,16000,100' )
        tof_params.meta['tip'] = "tof bin parameters (begin, end, step). units: us"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        tof_params = self.inventory.tof_params
        return ARCSxml, tof_params
        

    def _defaults(self):
        base._defaults(self)
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


from arcseventdata.pyre_support.AbstractHistogrammer import AbstractHistogrammer
class Engine(AbstractHistogrammer):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, tof_params):

        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']

        self._info.log( "eventdatafilename = %s" % eventdatafilename )
        self._info.log( "nevents = %s" % nevents )
        self._info.log( 'tof_params (unit: microsecond) = %s' % (tof_params, ) )

        import numpy
        tof_begin, tof_end, tof_step = numpy.array(tof_params)*1.e-6 #convert from microseconds to seconds

        import arcseventdata, histogram 
        tof_axis = histogram.axis(
            'tof',
            boundaries = histogram.arange(tof_begin, tof_end, tof_step),
            unit = 'second' )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpt)',
            detaxes + [tof_axis],
            data_type = 'int',
            )

        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )

        arcseventdata.events2Ipdpt(
            events, nevents, h )
        
        return h


def main():
    Application('ipdpt').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
