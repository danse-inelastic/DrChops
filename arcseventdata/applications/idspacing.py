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
## and create a histogram hdf5 file of I(dspacing)


from arcseventdata.pyre_support.MpiHistogrammerApp import Application as base


class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        from arcseventdata.pyre_support.Tuple import Tuple
        dspacingparams = Tuple( 't', default = '0,5,0.01' )
        dspacingparams.meta['tip'] = "d-spacing bin parameters (begin, end, step). units: angstrom"

        ARCSxml = pinv.str('x', default = "ARCS.xml")
        ARCSxml.meta['tip'] = "ARCS instrument xml"

        pass # end of Inventory


    def build_args(self):
        ARCSxml = self.inventory.ARCSxml
        dspacingparams = self.inventory.dspacingparams
        return ARCSxml, dspacingparams


    def _defaults(self):
        base._defaults(self)
        
        from arcseventdata.parallel_histogrammers.components.IdspacingHistogrammer import IdspacingHistogrammer as Engine
        self.inventory.engine = Engine( )
        return
    
    pass # end of Application



def main():
    Application('idspacing').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer1' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
