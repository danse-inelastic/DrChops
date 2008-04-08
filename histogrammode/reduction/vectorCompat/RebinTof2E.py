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

## \package reduction.vectorCompat.RebinTof2E
## rebin I(tof) --> I(E)
##
## Please note that this rebinner is different from 
## other similar rebinners. Some rebinners rebin tof to Ei-Ef,
## some may rebin tof to Ef-Ei, etc etc
## this rebinner simply rebin tof of neutron to energy of neutron.


import reduction.reduction as binding


bindings = {

    'npy_double': { 'ctor': binding.RebinTof2E,
                    '__call__': binding.RebinTof2E__call__numpyarray,
                    }

    }


class RebinTof2E:

    """Rebin I(tof) to I(E)

    only accepts numpy array.
    
    """

    def __init__(self, distance):
        """RebinTof2E(distance) -> engine to rebin tof to energy
        
        distance: in mm
        """
        self._distance = distance
        self._engines = {}
        return


    def __call__(self, tof, Itof, tmpE, E, IE):
        """rebinner( tof, Itof, tmpE, E, IE )
        rebin data in Itof to IE
        """
        type = self._checkType( tof, Itof, tmpE, E, IE)
        engine = self._getEngine( type )
        f = bindings[ type ]['__call__']
        f( engine, tof, Itof, tmpE, E, IE)
        return


    def _checkType(self, tof, Itof, tmpE, E, IE):
        if tof.dtype.char == 'd':
            return 'npy_double'
        raise NotImplementedError
        return


    def _getEngine(self, type):
        engine = self._engines.get( type )
        if engine is None:
            Engine = bindings[ type ][ 'ctor' ]
            self._engines[type] = engine = Engine(self._distance)
            pass
        return engine

    pass # end of RebinTof2E


# version
__id__ = "$Id$"

# End of file 
