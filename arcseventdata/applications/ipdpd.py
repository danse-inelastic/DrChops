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
        from arcseventdata.parallel_histogrammers.components.IpdpdHistogrammer import IpdpdHistogrammer as Engine

        self.inventory.engine = Engine( )
        return
    
    pass # end of Application


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
