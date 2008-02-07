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


## This script read events from ARCS event-mode preNexus file
## and write mslice spe and phx files


from ipdpE import Application as base

class Application( base ):

    class Inventory( base.Inventory  ):

        import pyre.inventory as pinv
        mslicefileprefix = pinv.str( 'mslice-prefix', default = 'mslice' )
        mslicefileprefix.meta['tip'] = 'prefix of mslice output files'
        pass # end of Inventory


    def _defaults(self):
        base._defaults(self)
        self.inventory.h5filename = 'IpdpE.h5'
        return


    def main(self):
        prefix = self.inventory.mslicefileprefix
        spef = '%s.spe' % prefix
        phxf = '%s.phx' % prefix
        if os.path.exists( spef ) or os.path.exists( phxf ):
            raise IOError , "%r or %r already exist" % (spef, phxf)
        
        base.main(self)

        from histogram.hdf import load
        h = load( self.inventory.h5filename, 'I(pdpE)' )

        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(self.inventory.ARCSxml)
        phi_p = infos['phis']
        psi_p = infos['psis']

        #convert to mslice file
        import arcseventdata
        arcseventdata.write_mslice_files( h, phi_p, psi_p, spef, phxf )
        return

    pass # end of Application

import os

def main():
    Application('idspacing').run( )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
