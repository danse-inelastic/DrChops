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
## and create a histogram hdf5 file of I(Qx, Qy, Qz, E)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        E_params = Tuple( 'E', default = '-50,50,10.' )
        E_params.meta['tip'] = "energy bin parameters (begin, end, step). units: meV"

        Qx_params = Tuple( 'Qx', default = '-10,10,1.' )
        Qx_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        Qy_params = Tuple( 'Qy', default = '-10,10,1.' )
        Qy_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        Qz_params = Tuple( 'Qz', default = '-10,10,1.' )
        Qz_params.meta['tip'] = "momentum transfer bin parameters (begin, end, step). units: angstrom**-1"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        Ei = pinv.float( 'I', default = 60 )
        Ei.meta['tip'] = 'incident energy. unit: meV'

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def main(self):
        self.compute()
        self.normalize()
        self.save()
        return


    def build_args(self):
        Qx_params = self.inventory.Qx_params
        Qy_params = self.inventory.Qy_params
        Qz_params = self.inventory.Qz_params
        E_params = self.inventory.E_params
        ARCSxml = self.inventory.ARCSxml
        Ei = self.inventory.Ei
        emission_time = self.inventory.emission_time
        return Qx_params, Qy_params, Qz_params, E_params, ARCSxml, Ei, emission_time
    
    
    def normalize(self):
        if self.mpiRank == 0:
            histogram = self.histogram
            self.histogram = self.inventory.engine.normalize( histogram )
        return
    
    
    def _defaults(self):
        base._defaults(self)
        from arcseventdata.parallel_histogrammers.components.IqqqeHistogrammer import IqqqeHistogrammer as Engine
        self.inventory.engine = Engine( )
        return


    def _init(self):
        base._init(self)
        return


    pass # end of Application



def main():
    Application('iqqqe').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer4' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
