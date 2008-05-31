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
## and create a histogram hdf5 file of I(tof)



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
        from arcseventdata.parallel_histogrammers.components.ItofHistogrammer import ItofHistogrammer as Engine
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application



def main():
    Application('itof').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer1' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
