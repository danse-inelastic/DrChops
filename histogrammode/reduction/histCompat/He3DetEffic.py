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


## \package reduction.histCompat.He3DetEffic


import journal
debug = journal.debug( 'reduction.histCompat.He3DetEffic' ) 

from pyre.units.pressure import atm
from pyre.units.length import cm
from histogram import unitFromString


class He3DetEffic:

    def __init__(self,
                 pressure=10.0*atm,
                 radius=2.5*cm,
                 nPoints=500,
                 dtype=6,
                 engine_factory = None,
                 costheta = 1.):
        if engine_factory is None:
            from reduction.vectorCompat.He3DetEffic import He3DetEffic
            engine_factory = He3DetEffic
            pass

        pressure = unitFromString( pressure )
        radius = unitFromString( radius )

        try:
            pressure + atm
            pressure = pressure/atm
        except:
            raise ValueError, "pressure has wrong unit: %s" % (pressure,)

        try:
            radius + cm
            radius = radius/cm
        except:
            raise ValueError, "radius has wrong unit: %s" % (radius,)

        debug.log( 'pressure: %s, radius: %s, nPoints: %s, dtype: %s' % (
            pressure, radius, nPoints, dtype ) )
        self._engine = engine_factory( pressure, radius, nPoints = nPoints, dtype = dtype, costheta = costheta )
        return


    def __call__(self, ef, detEfficHist = None):
        '''he3DetEffic( ef, detEfficHist ) --> varies

        if ef is an axis, then the detector efficiency histogram will be filled
        if ef is one number(with unit): then a single value will be calculated and
        returned.
        '''
        if isAxis(ef):
            efAxis = ef
            efAxis.changeUnit('meV')
            efsVect = efAxis.storage()
            detEfficVect = detEfficHist.data().storage()
            self._engine( efsVect, detEfficVect)
            return

        ef = ef/meV
        try:
            return self._engine( ef )
        except:
            raise ValueError , "ef is neither an axis not an energy value: %s" % (
                ef, )
        return

    pass # end of He3DetEffic


from pyre.units.energy import meV


def isAxis(candidate):
    from histogram.Axis import Axis
    return isinstance( candidate, Axis )


# version
__id__ = "$Id$"

# End of file 
