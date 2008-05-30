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
from reduction.pyre.inventory.Inventory import ObservableAdapter

from measurement.ins.ARCS.components.Measurement import Measurement as _L


class ARCSMeasurement( _L, MeasurementAdapter ):


    __doc__ = _L.__doc__


    class Inventory(ObservableAdapter,  _L.Inventory ):

        pass

    Inventory.mainrun.meta['importance'] = 1000
    Inventory.calibrun.meta['importance'] = 900
    #Inventory.vanadiumSampleFactory.meta['importance'] = 890
    Inventory.mtrun.meta['importance'] = 800
    #Inventory.mtCalib.meta['importance'] = 700
    

    def __init__(self, name = 'ARCSMeasurement' ):

        MeasurementAdapter.__init__(self, name )
        _L.__init__(self, name)
        return

    pass # end of ARCSMeasurement


# version
__id__ = "$Id$"

# End of file 
