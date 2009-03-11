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

        pack_params = Tuple( 'packs', default = '1,115' )
        pack_params.meta['tip'] = 'pack parameters (begin, end)'

        pixel_step = pinv.int( 'pixel-resolution', default = '1' )

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        tof_params = self.inventory.tof_params
        pack_params = self.inventory.pack_params
        pixel_step = self.inventory.pixel_step
        return ARCSxml, tof_params, pack_params, pixel_step
        

    def _defaults(self):
        base._defaults(self)
        from arcseventdata.parallel_histogrammers.components.IpdptHistogrammer import IpdptHistogrammer as Engine
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application



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
