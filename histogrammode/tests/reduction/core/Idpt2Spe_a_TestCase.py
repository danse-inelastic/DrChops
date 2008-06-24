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



import unittestX as unittest
import journal

debug = journal.debug( "Idpt2Spe_a_TestCase" )


from reduction.core.Idpt2Spe_a import Idpt2Spe_a



class Idpt2Spe_a_TestCase(unittest.TestCase):
     
    def _testCtor(self):
        "Idpt2Spe_a: ctor"
        reducer = Idpt2Spe_a(  )
        return


    def _testReduce2(self):
        "Idpt2Spe_a: reduce LRMECS data"

        import os
        f = os.path.join( curdir(), '..', '..', 'ins-data', 'Lrmecs', '4849' )
        from measurement.ins.LRMECS import createRun as createLrmecsRun
        run = createLrmecsRun( f )
        
        instrument, geometer = run.getInstrument()
        Idpt = run.getIdpt()
        
        reducer = Idpt2Spe_a( )

        from pyre.units.energy import meV
        ei = 59.1 * meV
        spehist = reducer(ei, Idpt, instrument, geometer)

        import pickle
        pickle.dump( spehist, open('simplespereducer-4849-spe.pkl', 'w') )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spehist )
        raw_input( 'Press <ENTER> to continue' )
        return


    def _testReduce3(self):
        "Idpt2Spe_a: reduce PHAROS data"

        import os
        datafile = os.path.join( curdir(), '..', '..', 'ins-data', 'Pharos', 'Pharos_342.nx.h5' )
        detdef = os.path.join( curdir(), '..', '..', 'ins-data', 'Pharos', 'PharosDefinitions.txt' )
        from measurement.ins.Pharos  import createRun as createPharosRun
        run = createPharosRun( detdef, datafile )
        
        instrument, geometer = run.getInstrument()
        Idpt = run.getIdpt()

        from histogram import axis, arange
        EAxis = axis('energy', arange( -60, 60, 1. ), unit = 'meV' )
        phiAxis = axis( 'phi', arange( 0, 150., 1.), unit = 'degree' )
        reducer = Idpt2Spe_a( phiAxis = phiAxis, EAxis = EAxis )

        ei = 75 * meV
        spehist = reducer(ei, Idpt, instrument, geometer)

        import pickle
        pickle.dump( spehist, open('simplespereducer-pharos342-spe.pkl', 'w') )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spehist )
        raw_input( 'Press <ENTER> to continue' )
        return


    def testReduce(self):
        "Idpt2Spe_a: reduce"
        from FakeMeasurement import Measurement
        from FakeInstrument import create as getInstr, R, numpxls, detradius, detpressure, numdets

        ei = 47.043 # v=3000m/s
        R = R/mm #
        scale_intensity = 3.0
        spe_standard_unit = meV

        from histogram import axis, arange
        EAxis = axis('energy', arange(-45, 45, 1.), unit='meV')
        phiAxis = axis('phi', arange(0.0, 100.0, 1.0), unit='degree')
        
        reducer = Idpt2Spe_a( EAxis = EAxis, phiAxis = phiAxis )

        instrument, geometer = getInstr()
        measurement = Measurement( instrument, geometer)
        mainrun = measurement.getRun("main")
        Idpt = mainrun.getIdpt()
        Idpt *= scale_intensity, 0
        spehist = reducer(ei*meV, Idpt, instrument, geometer)
        #import pickle
        #pickle.dump(spehist, open('spehist-FakeMeasurement.pkl', 'w') )

        testFacility = self

        def _check(sphiEHist):
            m = measurement

            #the thing to reduce
            h = m.getRun("main").getIdpt( None )
            
            #get info about tof axis
            tofAxis = h.axisFromName('tof')
            tofList = tofAxis.storage().asNumarray() * (tofAxis.unit()/microsecond)
            tofMin = tofList[0]; tofMax= tofList[-1]
            dtof = tofList[1] - tofList[0]
            
            # now get reduced S(E) obtained from reduction procedure
            # get s(phi,E) and then s(E) for a particular phi
            # we only check for one phi because all phi are equivalent
            phi, e, spe, err = _getPhiES(sphiEHist)

            # now try to calculate S(E) directly
            #   S(E) = S(tof) * (tof/2Ef) * (deltaE/deltaTof)
            # please take extra care when thinking about S(E) and S(tof)
            # S(...) is the number of counts in one bin (energy or time-of-flight)
            # it is not count density
            #
            # The term (tof/2Ef) is the jacobi of d(tof)/dE
            #
            # deltaE is the bin width of energy axis
            # deltaTof is the bin width of time-of-flight axis
            #ei = self.ei
                
            #jacobi = tof/2Ef
            jacobi = _calcJacobi(e, ei, R)
            debug.log( 'jacobi=%s'% jacobi )

            #energy axis
            EAxis = spehist.axisFromName( 'energy' )

            #deltaE
            de = e[1]-e[0]
                
            # deltaE/deltaTof
            deOverdtof = de/dtof
            debug.log( 'de/dtof = %s' % deOverdtof )

            #to calculate predictions, we need jacobi
            #every pixel in one detector tube has the same contribution.
            #numpxls is the number of pixels per tube
            counts = jacobi * deOverdtof * numpxls
            
            #print tofMin, tofMax
            
            eMin = _tof2e( tofMin, ei, R)
            eMax = _tof2e( tofMax, ei, R)
            #print eMax, eMin

            for detID in range(numdets):
                #FakeInstrument: phi = detID
                #so we can get slice this way:
                #s(E)
                se = spe[detID]
                #error of s(E)
                ee = err[detID]

                #calculate expected values
                #detector pressure
                pressure = detpressure(detID)
                #detector efficiency
                detEffHist = _calcDetEff(detradius, pressure, EAxis, ei)
                eff = detEffHist.data().storage().asNumarray().copy()

                #counts should be normalized by solid angle for a phi bin
                #now it is normalized by number of pixels
                #expected reduced intensity
                i_e = counts / eff / numpxls * scale_intensity
                #remember: it is the square of errors
                err_e = counts /eff/eff /numpxls/numpxls * scale_intensity  * scale_intensity 
                
                #now we can compare reduced data and computed data
                #plot to show comparison
                #import pylab
                #pylab.clf()
                #pylab.plot( e, se )
                #pylab.plot( e, i_e)
                #pylab.plot( e, se/i_e)
                #pylab.ylim( 0, 80 )
                #pylab.show()
                #raw_input("Press ENTER to continue")
                
                for i,energy_transfer in enumerate(e):
                    debug.line( 'w=%s'%energy_transfer )
                    if energy_transfer < eMax-2*de and \
                           energy_transfer > eMin+2*de:
                        debug.line("intensity: got %s, expected %s" % (
                            se[i], i_e[i]) )
                        debug.line(  "errors: got %s, expected %s" % (
                            ee[i], err_e[i]) )
                        testFacility.assertAlmostEqual( se[i], i_e[i], 0 )
                        #testFacility.assertAlmostEqual( ee[i], err_e[i], 0 )
                        pass
                    continue # e
                continue # detID
            debug.log( "done." )
            return

        
        def _tof2e(tof, ei, distSamp2Det):
            """convert tof to energy transfer
            """
            vf = distSamp2Det/tof*1000
            ef = 5.227e-6 * vf * vf
            return ei - ef


        def _calcDetEff(radius, pressure, EAxis, ei):
            """detector efficiency computation
            """
            from reduction.histCompat.He3DetEffic import He3DetEffic
            ECentersAxis = EAxis + (EAxis[1]-EAxis[0])/2
            efAxis = - ECentersAxis + ei*meV
            
            detEfficiency = He3DetEffic( pressure = pressure,
                                         radius = radius  )

            from histogram import histogram
            effHist = histogram( 'detEffic', [efAxis] )
            
            #debug.log( "efAxis=%s" % (efAxis.binCenters(),) )
            detEfficiency( efAxis, effHist )
            
            return effHist


        def _calcJacobi( e, ei, distSamp2Det):
            """
            calculate Jacobi of converting I(tof) to I(E)
            
            e: energy transfer
            ei: neutron incident energy
            distSamp2Det: distance from sample to detector
            """
            from numpy import array, sqrt
            ef = ei - array(e) #neutron final energy
            vf = sqrt( ef ) * 437.3949
            tof = distSamp2Det/vf*1000.
            jacobi = tof/2./ef
            return jacobi
        
        
        def _getPhiES( sphiEHist):
            """extract phi, E, S(phi,E) and error bars from sphiE histogram
            """
            from numpy import array
            phiaxis = sphiEHist.axisFromName( 'phi' )
            phi = array(phiaxis.binCenters())*(phiaxis.unit()/degree)
            eaxis = sphiEHist.axisFromName( 'energy' )
            e = array(eaxis.binCenters())*(eaxis.unit()/meV)
            
            spe = sphiEHist.I * sphiEHist.unit() * spe_standard_unit
            #spe = array(spe, copy = 1)
            spe.shape = len(phi), len(e)
                
            err = sphiEHist.E2 * sphiEHist.unit() * sphiEHist.unit() * spe_standard_unit * spe_standard_unit
            #err = array(err, copy = 1)
            err.shape = len(phi), len(e)
            return phi, e, spe, err

        _check( spehist )
        return

    pass

from pyre.units.energy import meV
from pyre.units.length import mm
from pyre.units.angle import degree
from pyre.units.time import microsecond
     
    
def curdir():
    import os
    return os.path.dirname( __file__ )
     
    
def pysuite():
    suite1 = unittest.makeSuite(Idpt2Spe_a_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('Idpt2Spe_a_TestCase').activate()
    #journal.debug('He3EfficiencyCorrection').activate()

    from reduction.core.Idpt2Spe_a import debug, info
    #debug.activate()

    #info.activate()

    #from reduction.histCompat.PhiRebinner import debug
    #debug.activate()

    #journal.debug( "RDriver" ).activate();

    from reduction.histCompat.He3DetEffic import debug
    #debug.activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
