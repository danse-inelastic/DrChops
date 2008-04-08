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


from Connectable import Connectable as base


class MaskFromUser(base):

    '''Detector mask

    Three inputs:
    
      - excludedDetectors
      - excludedPixels
      - excludedSingles
        '''


    class Inventory(base.Inventory):

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
    

    def __init__(self, name = 'maskFromUser'):
        base.__init__(self, name, facility='mask generator')
        return


    sockets = {
        'in': [],
        'out': ['mask'],
        }
    
    def _update(self):
        self._setOutput('mask', self._mask)
        return
    

    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.excludedSingles = eval(si.excludedSingles)
        self.excludedPixels = si.excludedPixels
        self.excludedDetectors = si.excludedDetectors
        return


    def _init(self):
        base._init(self)
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
