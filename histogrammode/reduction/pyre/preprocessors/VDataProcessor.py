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

## \package reduction.pyre.preprocessors.VDataProcessor


import reduction.units as units
meV = units.energy.meV

from Connectable import Connectable as base

class VDataProcessor(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv
        EiGuessForMainRun = pinv.dimensional( 'EiGuessForMainRun', default = 60*meV )
        EiGuessForMainRun.meta['tip'] = 'Incident neutron energy for the main experimental run'
        EiGuessForMainRun.meta['opacity'] = 10

        whitebeam = pinv.bool( 'whitebeam', default = True )
        whitebeam.meta['tip'] = "White beam run or not?"

        ei = pinv.dimensional( 'ei', default = 60*meV )
        ei.meta['tip'] = 'Incident neutron energy for the vanadium run. If white beam, this variable is meaningless'

        pass # end of Inventory


    def __init__(self, name= 'VDataProcessor'):
        base.__init__(self, name, facility = 'VDataProcessor' )
        return


    sockets = {
        'in': ['vanadium', 'ei_main'],
        'out': ['calibration constants', 'mask'],
        }

    def _update(self):
        engine = self._createEngine( )
        
        ei_main = self._getInput( 'ei_main' )
        mask = engine.getMask( ei_main )
        cc = engine.calibrationConstants( ei_main )

        self._setOutput( 'mask', mask )
        self._setOutput( 'calibration constants', cc )
        return
    

    def _createEngine(self):
        vanadiumRun = self._getInput( 'vanadium' )
        
        ei = self.ei
        whitebeam = self.whitebeam
        
        from reduction.core.VDataProcessor import VDataProcessor
        engine = VDataProcessor( vanadiumRun, 
                                 ei = ei, whitebeam = whitebeam )

        self._engine = engine
        return engine


    def _configure(self):
        base._configure(self)
        self.EiGuessForMainRun = self.inventory.EiGuessForMainRun
        self.setInput( 'ei_main', self.EiGuessForMainRun )
        self.ei = self.inventory.ei
        self.whitebeam = self.inventory.whitebeam
        return
    

    pass # end of VDataProcessor


# version
__id__ = "$Id: VDataProcessor.py 1270 2007-06-20 01:15:57Z linjiao $"

# End of file 
