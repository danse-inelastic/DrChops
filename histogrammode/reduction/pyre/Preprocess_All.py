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


#helper
from Connectable import Connectable
class GetRuns(Connectable):

    def __init__(self, name='getMain'):
        Connectable.__init__(self, name, 'facility')
        return

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'main', 'mt', 'vanadium' ],
        }

    def _update(self):
        measurement = self._getInput( 'measurement' )
        main = measurement.getRun('main')
        self._setOutput( 'main', main )

        vanadium = measurement.getRun('v')
        self._setOutput( 'vanadium', vanadium )

        mt = measurement.getRun('mt')
        self._setOutput( 'mt', mt )
        return

    pass # end of GetMain


from Composite import Composite as base


class Preprocess_All(base):

    '''Preprocessor that work on main sample run, emtpy-can run,
    and vanadium calibration run

    This component preprocess the three experimenal runs and return
    neutron incident energy and corrected I(det,pix,tof) histogram.

    This component first compute a detector mask out of vanadium
    calibration run, and add it to user-specified mask.
    Then it applies the mask to both main and emtpy-can data,
    subtracts time-independent background from both datasets,
    and normalizes both of them.
    Calibration constants are then applied to both datasets,
    before the emtpy-can dataset is subtracted from the main dataset.
    '''

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'Ei', 'Idpt', 'mask' ],
        }


    connections = [
        'self:measurement->measurement:getRuns',
        'getRuns:main->run:eiSolver:Ei->Ei:self',
        'eiSolver:Ei->ei_main:vDataProcessor',
        'getRuns:vanadium->vanadium:vDataProcessor',
        'vDataProcessor:mask->operand1:maskAdder',
        'maskFromUser:mask->operand2:maskAdder',
        'maskAdder:result->mask:preStep1_main',
        'maskAdder:result->mask:preStep1_mt',
        'vDataProcessor:calibration constants->calibration constants:calibrator_main',
        'vDataProcessor:calibration constants->calibration constants:calibrator_mt',
        'getRuns:main->run:preStep1_main:Idpt->histogram:calibrator_main:histogram->operand1:histogramSubtractor',
        'getRuns:mt->run:preStep1_mt:Idpt->histogram:calibrator_mt:histogram->operand2:histogramSubtractor',
        
        'maskAdder:result->mask:self',
        'histogramSubtractor:result->Idpt:self',
        ] 


    class Inventory(base.Inventory):

        import pyre.inventory as pinv
        
        f = pinv.facility

        getRuns = f('getRuns', default = GetRuns() )
        getRuns.meta['opacity'] = 1000
        
        from preprocessors.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as EiSolver
        eiSolver = f('eiSolver', default = EiSolver() )
        eiSolver.meta['opacity'] = 500

        from preprocessors.VDataProcessor import VDataProcessor
        vDataProcessor = f( 'vDataProcessor', default = VDataProcessor() )
        vDataProcessor.meta['importance'] = 10
        
        from Add import Add
        maskAdder = f('maskAdder', default = Add('maskAdder') )
        maskAdder.meta['opacity'] = 1000

        from preprocessors.MaskFromUser import MaskFromUser
        maskFromUser = f('maskFromUser', default = MaskFromUser() )
        maskFromUser.meta['importance'] = 800

        preStep1_main = f('preStep1_main', default = 'preStep1' )
        preStep1_main.meta['importance'] = 700
        preStep1_main.meta['opacity'] = 100
        
        preStep1_mt = f('preStep1_mt', default = 'preStep1' )
        preStep1_mt.meta['importance'] = 699
        preStep1_mt.meta['opacity'] = 100
        
        from preprocessors.Calibrator import Calibrator
        calibrator_main = f('calibrator_main', default = Calibrator('calibrator_main') )
        calibrator_main.meta['opacity'] = 1000
        
        from preprocessors.Calibrator import Calibrator
        calibrator_mt = f('calibrator_mt', default = Calibrator('calibrator_mt') )
        calibrator_mt.meta['opacity'] = 1000

        from InplaceSubtract import InplaceSubtract
        histogramSubtractor = f('histogramSubtractor', default = InplaceSubtract('histogramSubtractor' ) )
        histogramSubtractor.meta['opacity'] = 1000
        pass # end of Inventory


    def __init__(self, name='Preprocess_All' ):
        base.__init__(self, name)
        return

    pass # end of Preprocess_All
        


# version
__id__ = "$Id$"

# End of file 
