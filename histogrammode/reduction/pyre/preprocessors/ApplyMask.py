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


class ApplyMask(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def __init__(self, name='ApplyMask'):
        base.__init__(self, name, facility = 'mask applyer')
        return


    sockets = {
        'in': ['mask','Idpt'],
        'out': ['Idpt'],
        }


    def _update(self):
        Idpt = self._getInput( 'Idpt' )
        mask = self._getInput('mask')
        from reduction.core.ApplyMaskToHistogram import applyMask
        applyMask( mask, Idpt ) 
        self._setOutput( 'Idpt',  Idpt )
        return


    pass # end of ApplyMask



# version
__id__ = "$Id$"

# End of file 
