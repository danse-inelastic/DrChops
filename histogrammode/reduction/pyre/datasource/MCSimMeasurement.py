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


from MeasurementAdapter import MeasurementAdapter


from measurement.ins.MCSimulation.components.Measurement import Measurement as _L

from reduction.pyre.inventory.Inventory import ObservableAdapter


class MCSimMeasurement( _L, MeasurementAdapter ):

    __doc__ = _L.__doc__

    class Inventory( ObservableAdapter, _L.Inventory ):

        pass

    Inventory.main.meta['importance'] = 3000
    Inventory.calib.meta['importance'] = 900
    Inventory.vanadiumSampleFactory.meta['importance'] = 800
    Inventory.mt.meta['importance'] = 700
    Inventory.mtCalib.meta['importance'] = 600
    

    def __init__(self, name = 'MCSimMeasurement' ):

        MeasurementAdapter.__init__(self, name )
        _L.__init__(self, name)
        return

    pass # end of MCSimMeasurement


# version
__id__ = "$Id$"

# End of file 
