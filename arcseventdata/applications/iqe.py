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
        Q_params = self.inventory.Q_params
        E_params = self.inventory.E_params
        ARCSxml = self.inventory.ARCSxml
        Ei = self.inventory.Ei
        emission_time = self.inventory.emission_time
        return Q_params, E_params, ARCSxml, Ei, emission_time
    
    
    def normalize(self):
        if self.mpiRank == 0:
            histogram = self.histogram
            self.histogram = self.inventory.engine.normalize( histogram )
        return
    
    
    def _defaults(self):
        base._defaults(self)
        from arcseventdata.parallel_histogrammers.components.IqeHistogrammer import IqeHistogrammer as Engine
        self.inventory.engine = Engine( )
        return


    def _init(self):
        base._init(self)
        return


    pass # end of Application



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
