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
        'out': [ 'main', 'mt'],
        }

    def _update(self):
        measurement = self._getInput( 'measurement' )
        main = measurement.getRun('main')
        self._setOutput( 'main', main )

        mt = measurement.getRun('mt')
        self._setOutput( 'mt', mt )
        return

    pass # end of GetMain


from Composite import Composite as base


class Preprocess_Main_and_MT(base):

    '''Preprocessor that work on main sample run and the emtpy-can run.

    This component preprocess these two experimenal runs and return
    neutron incident energy and corrected I(det,pix,tof) histogram.

    This component applies a user-supplied mask to both main
    and emtpy-can data,
    subtracts time-independent background from both datasets,
    and normalizes both of them.
    In the last step, the emtpy-can dataset is subtracted from
    the main dataset.
    '''

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'Ei', 'Idpt', 'mask' ],
        }

    connections = [
        'self:measurement->measurement:getRuns',
        'getRuns:main->run:eiSolver:Ei->Ei:self',
        'maskFromUser:mask->mask:preStep1_main',
        'maskFromUser:mask->mask:preStep1_mt',
        'getRuns:main->run:preStep1_main:Idpt->operand1:histogramSubtractor',
        'getRuns:mt->run:preStep1_mt:Idpt->operand2:histogramSubtractor',
        'maskFromUser:mask->mask:self',
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

        from preprocessors.MaskFromUser import MaskFromUser
        maskFromUser = f('maskFromUser', default = MaskFromUser() )
        maskFromUser.meta['importance'] = 800

        preStep1_main = f('preStep1_main', default = 'preStep1' )
        preStep1_main.meta['importance'] = 700
        preStep1_main.meta['opacity'] = 100
        
        preStep1_mt = f('preStep1_mt', default = 'preStep1' )
        preStep1_mt.meta['importance'] = 699
        preStep1_mt.meta['opacity'] = 100

        from InplaceSubtract import InplaceSubtract
        histogramSubtractor = f('histogramSubtractor', default = InplaceSubtract('histogramSubtractor' ) )
        histogramSubtractor.meta['opacity'] = 1000
        pass # end of Inventory


    def __init__(self, name='Preprocess_Main_and_MT' ):
        base.__init__(self, name)
        return

    pass # end of Preprocess_Main_and_MT
        


# version
__id__ = "$Id$"

# End of file 
