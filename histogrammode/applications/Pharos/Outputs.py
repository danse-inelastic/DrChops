#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                       California Institue of Technology
#                            (C) Copyright 2006
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


from pyre.inventory.properties.String import String
class OutputDir(String):
    def __init__(self, name, **kwds):
        String.__init__(self, name, **kwds)
        self.type = "outputdir"
        return
    pass


class Outputs(Component):

    """This component collects settings of outputs.
    - output_dir: Where output data files should be saved
    - mslice: Whether mslice data files should be saved. 'mslice' is a famous
    program widely used in inelastic neutron scattering of single-crystals.
    Turn this option on so that mslice data files for the current datasets will
    be saved to 'output_dir'.
    Turn this option off will speed up the reduction a little bit.
    """

    class Inventory(Component.Inventory):
        import pyre.inventory as inv

        output_dir = OutputDir( "output-dir", default = '.' )
        output_dir.meta['tip'] = "Where output files should be saved?"
        output_dir.meta['importance'] = 100

        mslice = inv.bool("mslice", default = False )
        mslice.meta['tip'] = "Should we save mslice data files so that you can use mslice to look at the data in more details?"
        mslice.meta['importance'] = 10
        pass


    def __init__(self, name = "Outputs", facility = ""):
        Component.__init__(self, name, facility)
        return


    def _defaults(self):
        Component._defaults(self)
        import os
        self.inventory.output_dir = os.path.abspath( os.curdir )
        return


    def _init(self):
        Component._init(self)
        self._check_outdir( )
        return


    def _check_outdir(self):
        import os
        outdir = self.inventory.output_dir
        if outdir == "": outdir = self.inventory.output_dir = os.curdir
        if os.path.exists( outdir ) :
            if not os.path.isdir( outdir ):
                #if the given path is actually not a directory
                raise IOError , "%s is not a directory" % outdir
            #if the given path exists and is a directory, we are good
            pass
        else:
            #if the given path does not exist, create the path
            os.makedirs( outdir )
            pass
        return
    
    pass



# version
__id__ = "$Id: LrmecsReductionLight.py 1045 2006-08-02 01:35:32Z linjiao $"

# End of file 
