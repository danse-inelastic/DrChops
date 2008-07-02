#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.IncidentEnergySolver_UseMonitors
## Use monitor data to calculate incident neutron energy


from AbstractIncidentEnergySolver import AbstractIncidentEnergySolver as base


class IncidentEnergySolver_UseMonitors(base):
    
    """
    calcualte Ei from I(tof) data of two monitors.
    """


    def __init__(self, monitor1Id = 0, monitor2Id = 1,
                 monitor1tofrange = None,
                 monitor2tofrange = None,
                 monitor1FitGuess = None,
                 monitor2FitGuess = None,
                 fitter = None ):
        '''IncidentEnergySolver_UseMonitors( monitor1Id, monitor2Id,
    monitor1FitGuess = None, monitor2FitGuess = None, fitter = None )

    monitor1Id: id of the first (front) beam monitor
    monitor2Id: id of the second (back) beam monitor

    monitor1tofrange: a 2-tuple; tof range for monitor 1. None means full range
    monitor2tofrange: a 2-tuple; tof range for monitor 2. None means full range

    monitor1FitGuess(optional): guess of fitting parameter for first monitor.
    monitor2FitGuess(optional): guess of fitting parameter for second monitor.
    fitter(optional): simple fitting facility
    '''

        if monitor1FitGuess is None: monitor1FitGuess = defaultGuess
        if monitor2FitGuess is None: monitor2FitGuess = defaultGuess        

        debug.log( "monitor1Id=%s, monitor2Id=%s" % (
            monitor1Id, monitor2Id ) )
        self.monitor1Id = monitor1Id
        self.monitor2Id = monitor2Id
        self.monitor1tofrange = monitor1tofrange
        self.monitor2tofrange = monitor2tofrange
        self.monitor1FitGuess = monitor1FitGuess
        self.monitor2FitGuess = monitor2FitGuess
        
        if not fitter:
            from reduction.histCompat.PolynomialFitter import PolynomialFitter
            fitter = PolynomialFitter( 2 )
        self._fitter = fitter
        return
    
    
    def __call__(self, run):
        '''__call__( run )

        solve Ei for an experimental run.

        inputs:

          - run: an experimental run. instance of measurement.Run
        '''
        
        instrument, geometer = run.getInstrument()
        
        debug.log("monitor1Id: %s" % self.monitor1Id )
        debug.log("monitor2Id: %s" % self.monitor2Id )
        
        m1data = run.getMonitorItof( self.monitor1Id )
        m2data = run.getMonitorItof( self.monitor2Id )
        
        if self.monitor1tofrange: m1data = m1data[ self.monitor1tofrange ]
        if self.monitor2tofrange: m2data = m2data[ self.monitor2tofrange ]
        
        debug.log("m1data: %s" % (m1data.data().storage().asNumarray()) )
        debug.log("m2data: %s" % (m2data.data().storage().asNumarray()) )

        mon1Inits = self.monitor1FitGuess
        mon2Inits = self.monitor2FitGuess

        if self._isdefault(mon1Inits): mon1Inits = _guess( m1data )
        if self._isdefault(mon2Inits): mon2Inits = _guess( m2data )

        debug.log( "guess of monitor 1 peak: %s" % (mon1Inits,))
        debug.log( "guess of monitor 2 peak: %s" % (mon2Inits,))

        mon1 = instrument.getMonitors()[ self.monitor1Id ]
        mon2 = instrument.getMonitors()[ self.monitor2Id ]
        distance = geometer.distance( mon1, mon2 )

        from pyre.units.length import mm
        distance /= mm
        e = self._solve( distance, m1data, mon1Inits, m2data, mon2Inits )
        debug.log( "energy solved: %s" % e )
        from pyre.units.energy import meV
        return float(e) * meV
        

    def _solve(self, distance,
               m2Data, initVals2,
               m3Data, initVals3 ):
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
        dSq_m2_m3 = distance ** 2

        debug.log("d^2 = %s" % dSq_m2_m3)

        # cf Squires, eq 1-9 (ISBN 0-486-69447-X)
        self._ei = 5.227*dSq_m2_m3/tSq_m3_m2

        return self._ei

    
    def _isdefault(self, guess):
        assert len(guess) == 4, "guess should consits of four numbers: position, width, intensity, offset"
        for i in range(4):
            if abs(guess[i])>1.e-7: return False
        return True        


    def __fitMonitor( self, monitorData, gaussianGuess ):
        center, sigma, intensity, offset = gaussianGuess
        min = center - 2*sigma
        max = center + 2*sigma
        from histogram.SlicingInfo import SlicingInfo
        a = self._fitter.fit(
            monitorData[ SlicingInfo( (min, max) ) ], None )
        center = -a[1]/2./a[2]
        return center
    pass


#helpers
def _guess( monitorData ):
    "guess the position, width, and area of the peak in the given monior data"
    x = monitorData.axisFromId(1).binCenters()
    y = monitorData.data().storage().asNumarray()
    pos, height = _findMax(x,y)
    area = sum( y )*(x[1]-x[0])
    from math import sqrt, pi
    width = area/height/sqrt(pi)/2.
    return pos, width, area, 0.


def _findMax( xs, ys ):
    max = ys[0]; pos = xs[0]
    for x,y in zip(xs, ys):
        if y>max: max = y; pos =x
        continue
    return pos, max
        

defaultGuess = [0., 0., 0., 0.]

import journal
debug = journal.debug( "IncidentEnergySolver_UseMonitors" )


if __name__ == "__main__": main()
    
    

# version
__id__ = "$Id: EiSolverUsingMonitorData.py 1240 2007-03-27 19:58:24Z linjiao $"

# End of file 
