#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## This script reads events from event data file
## and create a histogram hdf5 file of I(pack, detector, pixel, Ei)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        Ei_params = Tuple( 'I', default = '0,100,1.' )
        Ei_params.meta['tip'] = "Ei bin parameters (begin, end, step). units: meV"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        emission_time = pinv.float( 't', default = 0)
        emission_time.meta['tip'] = 'emission time. tof reading - real tof. unit: microsecond'
        
        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        Ei_params = self.inventory.Ei_params
        emission_time = self.inventory.emission_time
        return ARCSxml, Ei_params, emission_time
        

    def _defaults(self):
        base._defaults(self)
        from arcseventdata.parallel_histogrammers.components.IpdpEiHistogrammer import IpdpEiHistogrammer as Engine

        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


def main():
    Application('ipdpI').run( )
    return


if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
