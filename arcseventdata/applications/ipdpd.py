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
        d_params = Tuple( 'd', default = '0,4.0,0.02' )
        d_params.meta['tip'] = "d-spacing bin parameters (begin, end, step). units: AA"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        d_params = self.inventory.d_params
        emission_time = self.inventory.emission_time
        return ARCSxml, d_params, emission_time
        

    def _defaults(self):
        base._defaults(self)
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


from arcseventdata.pyre_support.AbstractHistogrammer import AbstractHistogrammer
class Engine(AbstractHistogrammer):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, d_params,
              emission_time):
        
        self._info.log( "eventdatafilename = %s" % eventdatafilename )
        self._info.log( 'd_params (unit: AA) = %s' % (d_params, ) )
        self._info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
        self._info.log( 'neutrons: start = %d, n = %d' % (
            start, nevents ) )
    
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        d_begin, d_end, d_step = d_params # angstrom

        import arcseventdata, histogram 
        d_axis = histogram.axis('d spacing', boundaries = histogram.arange(
            d_begin, d_end, d_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpd)',
            detaxes + [d_axis],
            data_type = 'int',
            )

        self._info.log( "reading %d events..." % nevents )
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        self._info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        self._info.log( "histograming..." )
        arcseventdata.events2Ipdpd(
            events, nevents, h, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )

        self._info.log( "done histogramming." )
    
        return h


def main():
    Application('ipdpd').run( )
    return


if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
