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

## \package reduction.pyre.preprocessors.MeasurementAdapter
## 



from Connectable import Connectable as base

class MeasurementAdapter(base):


    def __init__(self, name, facility = 'measurement'):
        base.__init__(self, name, facility )
        return


    sockets = {
        'in': [],
        'out': ['measurement', 'instrument'],
        }
    

    def _update(self):
        self._setOutput( 'measurement', self.measurement )
        self._setOutput( 'instrument', self.measurement.getInstrument() )
        return

    pass # end of MeasurementAdapter


# version
__id__ = "$Id $"

# End of file 
