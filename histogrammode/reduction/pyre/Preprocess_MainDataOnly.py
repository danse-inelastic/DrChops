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
class GetMain(Connectable):

    def __init__(self, name='getMain'):
        Connectable.__init__(self, name, 'facility')
        return

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'main' ],
        }

    def _update(self):
        measurement = self._getInput( 'measurement' )
        main = measurement.getRun('main')
        self._setOutput( 'main', main )
        return

    pass # end of GetMain


from Composite import Composite as base


class Preprocess_MainDataOnly(base):

    '''Preprocessor that deals with main sample run only

    This component preprocess the main sample run and returns
    neutron incident energy and corrected I(det,pix,tof) histogram.
    '''

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'Ei', 'Idpt', 'mask' ],
        }

    connections = [
        'self:measurement->measurement:getMain',
        'getMain:main->run:eiSolver:Ei->Ei:self',
        'maskFromUser:mask->mask:preStep1',
        'maskFromUser:mask->mask:self',
        'getMain:main->run:preStep1:Idpt->Idpt:self',
        ] 

    class Inventory(base.Inventory):

        import pyre.inventory as pinv
        
        f = pinv.facility

        getMain = f('getMain', default = GetMain() )
        getMain.meta['opacity'] = 1000
        
        from preprocessors.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as EiSolver
        eiSolver = f('eiSolver', default = EiSolver() )
        eiSolver.meta['opacity'] = 1000

        from preprocessors.MaskFromUser import MaskFromUser
        maskFromUser = f('maskFromUser', default = MaskFromUser() )
        maskFromUser.meta['importance'] = 100

        preStep1 = f('preStep1', default = 'preStep1' )
        preStep1.meta['importance'] = 10
        preStep1.meta['opacity'] = 100
        
        pass # end of Inventory


    def __init__(self, name='Preprocess_MainDataOnly' ):
        base.__init__(self, name)
        return

    pass # end of Preprocess_MainDataOnly
        


# version
__id__ = "$Id$"

# End of file 
