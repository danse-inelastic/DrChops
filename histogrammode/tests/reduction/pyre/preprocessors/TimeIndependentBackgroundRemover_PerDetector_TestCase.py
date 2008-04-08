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


from FakeMeasurement import Measurement, signal
from FakeInstrument import create as getInstr



from pyre.applications.Script import Script

from unittestX import TestCase
class TimeIndependentBackgroundRemover_TestCase(TestCase):

    
    from reduction.pyre.preprocessors.TimeIndependentBackgroundRemover_PerDetector import TimeIndependentBackgroundRemover_PerDetector as Remover #overload this to test different sublass
    

    def test(self):
        """
        """
        testFacility = self
        bg = 0.5
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                timeBG = inv.facility( 'remover', factory = self.Remover )
                
                pass #


            def main(self):
                #prepare data
                instrument, geometer = getInstr()
                self.measurement = m = Measurement( instrument, geometer)
                self._hist = hist = m.getRun("main").getIdpt( None )

                #add some background to the histogram so we can see its effects
                self._addBG( hist )

                #dress up histogram to be a histogram collection
                from histogram.SimpleHistCollection import SimpleHistCollection
                mainHistCollection = SimpleHistCollection(hist)

                #do tbg processing
                #tof indenpendent background is assumed to be at tof  0
                tbgMin, tbgMax = self.tbgRange()

                self.timeBG.setInput( 'tofWindow', (tbgMin, tbgMax) )
                from instrument.DetectorMask import DetectorMask
                mask = DetectorMask()

                self.timeBG.setInput('mask', mask)

                for hist in mainHistCollection:
                    self.timeBG.setInput('histogram', hist )
                    self.timeBG.getOutput( 'histogram' )
                    continue


                self.timeBG.bg()
                #check whether timeBG works well
                self._check(hist)
                return


            def tbgRange(self):
                hist = self._hist
                tofBBs = hist.axisFromName('tof').binCenters()
                return tofBBs[0], tofBBs[2]


            def _addBG(self, hist):
                "add a fake background"
                
                tbgMin, tbgMax = self.tbgRange()
                bgSlice = hist[(), (), (tbgMin, tbgMax)]
                bgSlice.data()[:] = bgSlice.errors()[:] = bg
                return
            

            def _check(self, hist):
                data = hist.data().storage().asNumarray()
                errs = hist.errors().storage().asNumarray()
                shape = errs.shape = data.shape = hist.shape()
                tofs = hist.axisFromName('tof').binCenters()

                ndets, npxls, ntofbins = shape

                residual = signal - bg

                tbgMin, tbgMax = self.tbgRange()

                for detIdx in range(ndets):
                    for pxlIdx in range(npxls):
##                         print data[detIdx, pxlIdx]
##                         continue
                        for tofBin in range(ntofbins):
                            #print detIdx, pxlIdx, tofBin
                            if tofs[tofBin] > tbgMax or tofs[tofBin] < tbgMin:
                                testFacility.assertAlmostEqual(
                                    data[detIdx, pxlIdx, tofBin], residual)
                                pass
                            continue
                        continue
                    continue
                return


            def _defaults(self):
                Script._defaults(self)
                si = self.inventory
                return


            def _configure(self):
                si = self.inventory
                self.timeBG = si.timeBG
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of TimeIndependentBackgroundRemover_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TimeIndependentBackgroundRemover_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('vectorCompat.ERebinAllInOne').activate()
    journal.debug('Rebinner').activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('TBGProcessor').activate()
    journal.debug('BGAccumulator').activate()
    journal.debug('TBGProcessorPerDet').activate()
    journal.info('TBGProcessorPerDet').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: TimeIndependentBackgroundRemover_PerDetector_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
