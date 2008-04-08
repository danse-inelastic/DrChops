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


## \package reduction.histCompat.RebinTof2E
## rebin I(tof) --> I(E)
##
## Please note that this rebinner is different from 
## other similar rebinners. Some rebinners rebin tof to Ei-Ef,
## some may rebin tof to Ef-Ei, etc etc
## this rebinner simply rebin tof of neutron to energy of neutron.



class RebinTof2E:

    """Rebin I(tof) to I(E)
    """

    def __init__(self, distance):
        """RebinTof2E(distance) -> engine to rebin tof to energy
        
        distance: distance (must have units attached)
        """
        self._createEngine(distance)
        self._tmpE = None
        return


    def setDistance(self, distance):
        self._createEngine(distance)
        return


    def __call__(self, Itof, IE):
        """rebinner( Itof, IE )
        
        rebin histogram in Itof to IE
        """
        tofAxis = Itof.axisFromName('tof')
        tofAxis.changeUnit( 'microsecond' )
        tof = tofAxis.storage().asNumarray()
        
        if self._tmpE is None or self._tmpE.size != tofAxis.size():
            self._tmpE = tof.copy()
        tmpE = self._tmpE

        EAxis = IE.axisFromName('energy')
        EAxis.changeUnit( 'meV' )
        E = EAxis.storage().asNumarray()

        engine = self._engine

        Itof_data = Itof.data().storage().asNumarray()
        IE_data = IE.data().storage().asNumarray()
        engine( tof, Itof_data, tmpE, E, IE_data)

        Itof_errors = Itof.errors().storage().asNumarray()
        IE_errors = IE.errors().storage().asNumarray()
        engine( tof, Itof_errors, tmpE, E, IE_errors)
        
        return


    def _createEngine(self, distance ):
        from reduction.vectorCompat.RebinTof2E import RebinTof2E
        from pyre.units.length import mm
        self._engine = RebinTof2E( distance/mm )
        return

    pass # end of RebinTof2E


# version
__id__ = "$Id$"

# End of file 
