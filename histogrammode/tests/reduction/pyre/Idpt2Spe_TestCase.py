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


import unittest


from FakeMeasurement import Measurement
from FakeInstrument import create as getInstr, R
from FakeInstrument import numpxls


from pyre.applications.Script import Script

from unittestX import TestCase
class Idpt2Spe_TestCase(TestCase):


    from reduction.pyre.Idpt2Spe import Idpt2Spe as Idpt2Spe #override this to test another Idpt2Spe
    

    def test(self):
        """
        """
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv
            
                reducer = inv.facility( 'reducer', factory = self.Idpt2Spe )
                
                pass #


            def main(self):
                #prepare data
                instrument, geometer = getInstr()
                self.instrument = instrument
                self.measurement = m = Measurement( instrument, geometer)
                #self._debug.log( "histogram: %s" % m.getRun("main").getIdpt().data().storage().asList() )
                
                self.ei = ei = 47.043 * meV # v=3000m/s

                #do reduction
                reducer = self.inventory.reducer

                sphiEHist = reducer(
                    ei,
                    m.getRun("main").getIdpt(),
                    instrument, geometer)

                #compare reduced data to direct computatiion
                self._check(sphiEHist)
                return
            

            def _check(self, sphiEHist):
                instrument = self.instrument
                #get info about tof axis
                m = self.measurement
                h = m.getRun("main").getIdpt( None )
                tofAxis = h.axisFromName('tof')
                tofAxis.changeUnit( 'microsecond' )
                tofList = tofAxis.storage().asList()
                tofMin = tofList[0]; tofMax= tofList[-1]
                dtof = tofList[1] - tofList[0]

                # now get reduced S(E) obtained from reduction procedure
                # get s(phi,E) and then s(E) for a particular phi
                # we only check for one phi 
                phi, e, spe, err = self._getPhiES(sphiEHist)
                #s(E)
                se = spe[0]
                #error of s(E)
                ee = err[0] 
                #detector system
                detsys = instrument.getDetectorSystem()
                #the first detector
                detector = detsys.elements()[0]

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
                ei = self.ei
                
                #jacobi = tof/2Ef
                jacobi = self._calcJacobi(e, ei/meV, R/mm)
                self._debug.log( 'jacobi=%s'% jacobi )

                #detector efficiency
                detEffHist = self._calcDetEff(e, ei/meV, detector)
                eff = detEffHist.data().storage().asNumarray().copy()
                self._debug.log( 'det eff = %s' % eff )

                #deltaE
                de = e[1]-e[0]
                
                # deltaE/deltaTof
                deOverdtof = de/dtof
                self._debug.log( 'de/dtof = %s' % deOverdtof )

                # calculate predictions
                #every pixel in one detector tube has the same contribution.
                #numpxls is the number of pixels per tube
                counts = jacobi * deOverdtof * numpxls
                #counts should be normalized by solid angle for a phi bin
                #now it is normalized by number of pixels: Idpt2Spe._calcSolidAngleNormalizer
                i_e = counts / eff / numpxls
                #remember: it is the square of errors
                err_e = counts /eff/eff /numpxls/numpxls

                #now we can compare reduced data and computed data
                #plot to show comparison
                import pylab
                pylab.clf()
                pylab.plot( e, se )
                pylab.plot( e, i_e)
                pylab.ylim( 0, 80 )
                pylab.show()
                #print tofMin, tofMax
                eMin = self._tof2e( tofMin, ei/meV, R/mm)
                eMax = self._tof2e( tofMax, ei/meV, R/mm)
                #print eMax, eMin
                for i,energy_transfer in enumerate(e):
                    self._debug.line( 'w=%s'%energy_transfer )
                    if energy_transfer < eMax-2*de and energy_transfer > eMin+2*de:
                        self._debug.line(  "intensity: got %s, expected %s" % (se[i], i_e[i]) )
                        self._debug.line(  "errors: got %s, expected %s" % (ee[i], err_e[i]) )
                        testFacility.assertAlmostEqual( se[i], i_e[i], 0 )
                        #testFacility.assertAlmostEqual( ee[i], err_e[i], 1 )
                        pass
                    continue
                self._debug.log( "done." )
                return


            def _tof2e(self, tof, ei, distSamp2Det):
                """convert tof to energy transfer
                """
                vf = distSamp2Det/tof*1000
                ef = 5.227e-6 * vf * vf
                return ei - ef


            def _calcDetEff(self, e, ei, detector):
                """detector efficiency computation
                """
                instrument, geometer = getInstr()
                from reduction.core.DetEfficiency import DetEfficiency
                detEff = DetEfficiency( )
                from histogram import axis
                eAxis = axis( 'energy', e, unit = 'meV')
                efAxis = - eAxis + ei * meV
                return detEff.efficiency_vs_energy( detector, efAxis )


            def _calcJacobi(self, e, ei, distSamp2Det):
                """
                calculate Jacobi of converting I(tof) to I(E)
                
                e: energy transfer
                ei: neutron incident energy
                distSamp2Det: distance from sample to detector
                """
                from numpy import array, sqrt
                ef = ei - array(e) #neutron final energy in meV
                vf = sqrt( ef ) * 437.3949
                tof = distSamp2Det/vf*1000.
                jacobi = tof/2./ef
                return jacobi


            def _getPhiES(self, sphiEHist):
                """extract phi, E, S(phi,E) and error bars from sphiE histogram
                """
                from numpy import array
                phi = sphiEHist.axisFromName('phi').binCenters()
                e = sphiEHist.axisFromName('energy').binCenters()
                
                spe = sphiEHist.data().storage().asNumarray()
                spe = array(spe, copy = 1)
                spe.shape = len(phi), len(e)
                
                err = sphiEHist.errors().storage().asNumarray()
                err = array(err, copy = 1)
                err.shape = len(phi), len(e)
                return phi, e, spe, err


            def _defaults(self):
                Script._defaults(self)
                si = self.inventory
                reducer = si.reducer
                ri = reducer.inventory
                from reduction.pyre.Axis import Axis
                ri.EAxis = Axis( 'energy', -45.0, 45.0, 1.0, 'meV')
                ri.phiAxis = Axis( "phi", 0.0, 100.0, 1.0, 'degree')
                return


            def _configure(self):
                si = self.inventory
                self.reducer = si.reducer
                return

            pass #
        
        t = Test('Idpt2Spe_TestCase')
        t.run()
        return
    
    pass # end of Idpt2Spe_TestCase


from pyre.units.energy import meV
from pyre.units.length import mm

import unittest

def pysuite():
    suite1 = unittest.makeSuite(Idpt2Spe_TestCase)
    return unittest.TestSuite( (suite1,) )


import journal
##     journal.debug('vectorCompat.ERebinAllInOne').activate()
##     journal.debug('Rebinner').activate()
#journal.debug('Idpt2Spe_TestCase').activate()
#journal.debug('Idpt2Spe').activate()
#journal.debug('Idpt2Spe_Parallel').activate()
#journal.debug("NdArrayDataset").activate()

def main():
    journal.debug('Idpt2Spe_TestCase').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Idpt2Spe_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
