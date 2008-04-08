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


#helper
from Connectable import Connectable
class _Measurement(Connectable):

    def __init__(self, name='_Measurement'):
        Connectable.__init__(self, name, 'facility')
        return

    sockets = {
        'in': [ 'measurement' ],
        'out': [ 'measurement', 'instrument' ],
        }

    def _update(self):
        measurement = self._getInput( 'measurement' )
        instrument, g = measurement.getInstrument()
        self._setOutput( 'measurement', measurement )
        self._setOutput( 'instrument', (instrument,g) )
        return

    pass # end of GetMain


from datasource.LrmecsMeasurement import LrmecsMeasurement
from Preprocess_MainDataOnly import Preprocess_MainDataOnly
from Idpt2Spe import Idpt2Spe

from Composite import Composite  as base


class SpeReducer(base):

    '''Reduce experimental data to S(phi,E)

    This reducer makes use of a Preprocessing component to preprocess
    the raw experimental data and perform corrections, 
    and a Idpt2Spe processing component that convert I(det,pix,tof)
    to S(phi,E).
    '''

    class Inventory( base.Inventory ):
        import pyre.inventory as inv

        _Measurement = inv.facility(
            '_Measurement', factory = _Measurement )
        _Measurement.meta['opacity'] = 1000

        preprocess = inv.facility(
            'preprocess', factory = Preprocess_MainDataOnly )
        preprocess.meta['importance'] = 900
        
        Idpt2Spe = inv.facility(
            'Idpt2Spe', factory = Idpt2Spe )
        Idpt2Spe.meta['importance'] = 800

        pass #


    connections = [
        'self:measurement->measurement:_Measurement',
        '_Measurement:measurement->measurement:preprocess',
        '_Measurement:instrument->instrument:Idpt2Spe',
        'preprocess:Idpt->Idpt:Idpt2Spe',
        'preprocess:Ei->Ei:Idpt2Spe',
        'preprocess:mask->mask:Idpt2Spe',
        'Idpt2Spe:spe->spe:self',
        'preprocess:Ei->Ei:self',
        ]

    sockets = {
        'in': ['measurement'],
        'out': ['spe', 'Ei'],
        }


    def __init__(self, name='SpeReducer'):
        base.__init__(self, name, 'SpeReducer' )
        return


    def _configure(self):
        base._configure(self)
        return


    def _init(self):
        base._init(self)
        return

    pass #
        
    

# version
__id__ = "$Id: SpeReducer.py 1371 2007-08-06 06:02:00Z linjiao $"

# End of file 
