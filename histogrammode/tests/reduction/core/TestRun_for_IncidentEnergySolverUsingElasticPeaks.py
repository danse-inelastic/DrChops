
import journal
jnltag = 'TestRun_for_IncidentEnergySolverUsingElasticPeaks'
debug = journal.debug(jnltag)

#a simple peak function
from numpy import exp
def peak( x, x0, ht, width ):
    return ht * exp( -( (x-x0)/width ) ** 2 )

#create a run class. only the method "getDetPixTOFHistCollection"
#is used

#use an artificial instrument configuration to do the test
#the special instrument has detectors arranged as a partial
#cylinder.
import instrument.factories.Instrument_CylindricalDetectorSystem as InstrumentFactory
factory = InstrumentFactory.InstrumentFactory()
instrument, geometer = factory.construct()


from pyre.units import energy, SI, time
# some parameters 
velocity = 5000. * SI.meter/SI.second 
ei = (velocity/SI.meter*SI.second) **2 * 5.227e-6 * energy.meV
mod2sample = InstrumentFactory.mod2sample

# instrument 
sample2det = InstrumentFactory.R
pixelHeight = InstrumentFactory.pixelHeight
meantof = (sample2det + mod2sample)/velocity 
tofaxisrange = meantof - time.millisecond, meantof + time.millisecond
tofpeakwidth = 20. #microsecond
tofpeakheight = 10.

nTotDets = InstrumentFactory.numdets
nPixels = InstrumentFactory.numpxls


class Run:

    def getInstrument(self):
        return instrument, geometer

    def getIdpt(self, detectorID = None):
        from histogram import histogram, datasetFromFunction, axis, arange
        detIDs = range( nTotDets )
        pixIDs = range( nPixels )
        detectorIDaxis = axis( "detectorID", detIDs )
        pixelIDaxis = axis( "pixelID", pixIDs )
        tofmin, tofmax = tofaxisrange
        microsecond = time.microsecond
        tofaxis = axis(
            'tof', arange(tofmin/microsecond, tofmax/microsecond, 1.), unit = microsecond)

        idpt = histogram(
            'idpt', (detectorIDaxis, pixelIDaxis, tofaxis) )

        from math import sqrt

        for pixID in pixIDs:
            y = (pixID - (nPixels-1)/2.)* pixelHeight
            sample2pixel = ( y**2 + sample2det**2 ) ** 0.5
            totdist = mod2sample + sample2pixel
            debug.log( 'totdist = %s' % totdist )
            tofcenter = totdist/velocity 
            tofcenterus = tofcenter/microsecond
            debug.log( "tofcenterus=%s" % tofcenterus )
            def peak1(tof):
                return peak(
                    tof, tofcenterus, tofpeakheight, tofpeakwidth )
            curve = datasetFromFunction( peak1, (tofaxis,) )
            for detID in detIDs:
                idpt[ detID, pixID, () ] = curve, curve
                continue
            continue
        return idpt
    pass


