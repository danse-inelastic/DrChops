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
        E_params = Tuple( 'E', default = '-50,50,1.' )
        E_params.meta['tip'] = "energy bin parameters (begin, end, step). units: meV"

        ARCSxml = pinv.str('x', default = "ARCSxml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        Ei = pinv.float( 'I', default = 60 )
        Ei.meta['tip'] = 'incident energy. unit: meV'

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        E_params = self.inventory.E_params
        Ei = self.inventory.Ei
        emission_time = self.inventory.emission_time
        return ARCSxml, E_params, Ei, emission_time
        

    def _defaults(self):
        base._defaults(self)
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


from arcseventdata.pyre_support.AbstractHistogrammer import AbstractHistogrammer
class Engine(AbstractHistogrammer):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, E_params,
              Ei, emission_time):
        
        self._info.log( "eventdatafilename = %s" % eventdatafilename )
        self._info.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        self._info.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
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
    
        E_begin, E_end, E_step = E_params # angstrom

        import arcseventdata, histogram 
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpE)',
            detaxes + [E_axis],
            data_type = 'int',
            )

        self._info.log( "reading %d events..." % nevents )
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        self._info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        self._info.log( "histograming..." )
        arcseventdata.events2IpdpE(
            events, nevents, h, Ei, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )

        self._info.log( "done histogramming." )
    
        return h


def main():
    Application('ipdpE').run( )
    return


if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
