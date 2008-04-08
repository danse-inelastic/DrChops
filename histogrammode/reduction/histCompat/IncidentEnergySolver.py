#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.histCompat.IncidentEnergySolver
## find out incident neutron energy from monitor data. A histCompat fitter is
## used to fit the peak in the monitor data and find out tofs, which,
## in turn, is used to calculate neutron energy.


from math import sqrt

import journal
debug = journal.debug( "reduction.histCompat")


class IncidentEnergySolver( object):

    def ei( self):
        """ei() -> most recently solved energy, in meV"""
        return self._ei
    

    def solve( self, m2Data, m3Data, initVals2, initVals3):
        """solve( m2Data, m3Data, initVals2, initVals3) -> e_i (probably meV)
        determine the energy of the peak seen in monitor2 and monitor3.
        Inputs:
            m2Data: MonitorData object for monitor2 (immed. aft Fermi chopper)
            m3Data: MonitorData object for monitor3 (near beam stop)
            initVals2(3): list of initial values for fit parameters
                          standard params are
                          x0.........Gaussian peak position
                          sigma......Gaussian peak width
                          I..........Gaussian peak integrated intensity
                          a..........constant offset
        Output:
            incident energy
        Exceptions: ??
        Notes: (1) If MonitorData are given in correct units (such as mm for
               distance and microseconds for time), e_i will be in meV. If not,
               not.
               (2) initial values for fit parameters are passed as a whole to
               the fitting routine, so if you use a fit function with a
               different parameters, just pass an appropriate list to
               solve().
        """
        # fit monitor2
        mon2Fit = self.__fitMonitor( m2Data, initVals2)

        debug.log("fit for monitor 2: %s" % mon2Fit)

        # fit monitor3
        mon3Fit = self.__fitMonitor( m3Data, initVals3)

        debug.log("fit for monitor 3: %s" % mon3Fit)

        # square of time from m2 to m3
        tSq_m3_m2 = (mon3Fit - mon2Fit)**2

        debug.log("t^2 = %s" % tSq_m3_m2)

        # square of distance from m2 to m3
        dispSq_m2_m3 = [(a1 - a2)**2 for (a1,a2) in
                        zip( m2Data.cartesianPosition(),
                             m3Data.cartesianPosition())]
        dSq_m2_m3 = sum( dispSq_m2_m3)

        debug.log("d^2 = %s" % dSq_m2_m3)

        # cf Squires, eq 1-9 (ISBN 0-486-69447-X)
        self._ei = 5.227*dSq_m2_m3/tSq_m3_m2
        
        return self._ei


    def __init__( self, fitter=None):
        if not fitter:
            from reduction.histCompat.PolynomialFitter import PolynomialFitter
            fitter = PolynomialFitter( 2 )
        self._fitter = fitter
        return


    def __fitMonitor( self, monitorData, gaussianGuess ):
        center, sigma, intensity, offset = gaussianGuess
        min = center - 2*sigma
        max = center + 2*sigma
        from histogram.SlicingInfo import SlicingInfo
        a = self._fitter.fit( monitorData[ SlicingInfo( (min, max) ) ], None )
        center = - a[1]/a[2]/2.
        return center

        

# version
__id__ = "$Id: IncidentEnergySolver.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
