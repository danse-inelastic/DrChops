#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component


class Mask(Component):


    class Inventory(Component.Inventory):

        import pyre.inventory as inv
        
        # excluded detectors
        excludedDetectors = inv.slice("excludedDetectors", default = [])
        excludedDetectors.meta['tip'] = "id's of detectors to exclude all pixels"
        
        # excluded pixels
        excludedPixels = inv.slice("excludedPixels", default = [])
        excludedPixels.meta['tip'] = "id's of pixels to exclude from all detectors"

        # excluded singles:
        excludedSingles = inv.str("excludedSingles", default = '[]')
        excludedSingles.meta['tip'] = "(detID, pixID) of single pixels to exclude"

        pass # end of Inventory
    

    def __init__(self, name = 'mask'):
        Component.__init__(self, name, facility='facility')
        return


    def __call__(self):
        return self._mask


    def _configure(self):
        Component._configure(self)
        si = self.inventory
        self.excludedSingles = eval(si.excludedSingles)
        self.excludedPixels = si.excludedPixels
        self.excludedDetectors = si.excludedDetectors
        return


    def _init(self):
        Component._init(self)
        from instrument import mask
        self._mask = mask(
            excludedDetectors = self.excludedDetectors,
            excludedPixels = self.excludedPixels,
            excludedSingles = self.excludedSingles )
        return


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Fri Jun 29 18:02:59 2007

# End of file 
