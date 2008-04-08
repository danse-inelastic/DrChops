
#a simple peak function
from numpy import exp
def peak( x, x0, ht, width ):
    return ht * exp( -( (x-x0)/width ) ** 2 )

#create a run class. since only the method "getMonitorItof"
#is used by IncidentEnergySolver_UseMonitors, this class can be really simple
velocity = 5000. #m/s
ei = velocity **2 * 5.227e-6 #meV
dist1 = 1. #m
dist2 = 2. #m
nBins = 40
dTof = 1.0 #musec

#minimal interface for instrument hierarchy
class Monitor:
    def __init__(self, guid): self._guid = guid
    pass

class Instrument:

    def getMonitors(self): return self._monitors

    def __init__(self): self._monitors = {}

    def addMonitor(self, m, id): self._monitors[id] = m

    pass # end of Instrument

m1 = Monitor(100)
m2 = Monitor(1000)

instrument = Instrument()

instrument.addMonitor(m1, 1)
instrument.addMonitor(m2, 2)


# minimal interface for geometr
class Geometer:

    def distance(self, element1ID, element2ID):
        from pyre.units.length import meter
        #must return with unit
        return (dist2 - dist1)* meter

geometer = Geometer()


class Run:

    def getInstrument(self):
        return instrument, geometer

    def getMonitorItof(self, monitorId):
        if monitorId == 1: return self._m1()
        elif monitorId == 2: return self._m2()
        raise "Incorrect monitor id %s" % monitorId

    def _m1(self): return self._createMonData( dist1 )

    def _m2(self): return self._createMonData( dist2 )

    def _createMonData(self, distance):
        tofCenter = distance/velocity*1e6 #musec

        t0 = tofCenter-nBins*dTof/2.
        t1 = t0 + dTof*nBins

        from histogram import axis, datasetFromFunction, histogram, arange
        tofAxis = axis(
            name="tof", unit="microsecond",
            centers = arange( t0, t1, dTof ) )

        ret = histogram("monitor data", [ tofAxis ] )

        def f( tof ):
            return peak(tof, tofCenter, 100., dTof*10 )
        I = datasetFromFunction( f, [tofAxis] )
        ret[()] = I,I

        return ret
    pass

