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
## and create a histogram hdf5 file of I(Q, E)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        E_params = Tuple( 'E', default = '-50,50,1.' )
        E_params.meta['tip'] = "energy bin parameters (begin, end, step). units: meV"

        Q_params = Tuple( 'Q', default = '0,13,1.' )
        Q_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        ARCSxml = pinv.str('x', default = "ARCSxml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        Ei = pinv.float( 'I', default = 60 )
        Ei.meta['tip'] = 'incident energy. unit: meV'

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def build_args(self):
        Q_params = self.inventory.Q_params
        E_params = self.inventory.E_params
        ARCSxml = self.inventory.ARCSxml
        Ei = self.inventory.Ei
        emission_time = self.inventory.emission_time
        return Q_params, E_params, ARCSxml, Ei, emission_time
        

    def _defaults(self):
        base._defaults(self)
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application



from arcseventdata.pyre_support.AbstractHistogrammer import AbstractHistogrammer
class Engine(AbstractHistogrammer):

    def _run( self,
              eventdatafilename, start, nevents,
              Q_params, E_params, ARCSxml, Ei, emission_time):
        
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        self._debug.log( "eventdatafilename = %s" % eventdatafilename)
        self._debug.log( "nevents = %s" % nevents)
        self._debug.log( "pixel-positions-filename=%s" % pixelPositionsFilename)
        self._debug.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        self._debug.log( 'Q_params (unit: angstrom^-1) = %s' % (Q_params, ) )
        self._debug.log( 'mod2sample distance = %s' % mod2sample )
        self._debug.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        self._debug.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        E_begin, E_end, E_step = E_params # meV
        Q_begin, Q_end, Q_step = Q_params # angstrom^-1
        
        import arcseventdata, histogram 
        Q_axis = histogram.axis('Q', boundaries = histogram.arange(
            Q_begin, Q_end, Q_step) )
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        h = histogram.histogram(
            'I(Q,E)',
            [
            Q_axis,
            E_axis,
            ],
            data_type = 'int',
            )

        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename )
        
        arcseventdata.events2IQE(
            events, nevents, h, Ei, pixelPositions,
            npacks = npacks, ndetsperpack = ndetsperpack,
            npixelsperdet = npixelsperdet,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )
    
        return h

    pass # end of Engine


def main():
    Application('iqe').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
