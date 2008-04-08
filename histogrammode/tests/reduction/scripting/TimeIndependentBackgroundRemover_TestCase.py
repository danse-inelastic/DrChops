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


import unittestX as unittest


from FakeMeasurement import Measurement, signal
from FakeInstrument import main as getInstr
from reduction.scripting import removeTIBG


class TimeBG_TestCase(unittest.TestCase):


    def test(self):
        """TimeIndependentBackgroundRemover
        """

        def tbgRange(hist):
            tofBBs = hist.axisFromName('tof').binCenters()
            return tofBBs[0], tofBBs[2]


        def _addBG(hist):
            "add a fake background"
                
            tbgMin, tbgMax = tbgRange(hist)
            bgSlice = hist[(), (), (tbgMin, tbgMax)]
            bgSlice.data()[:] = bgSlice.errors()[:] = bg
            return
            

        def _check(hist):
            data = hist.data().storage().asNumarray()
            errs = hist.errors().storage().asNumarray()
            shape = errs.shape = data.shape = hist.shape()
            tofs = hist.axisFromName('tof').binCenters()

            ndets, npxls, ntofbins = shape

            residual = signal - bg

            tbgMin, tbgMax = tbgRange(hist)

            for detIdx in range(ndets):
                for pxlIdx in range(npxls):
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

        testFacility = self
        bg = 0.5
        
        #prepare data
        instrument, geometer = getInstr()
        measurement = m = Measurement( instrument, geometer)
        hist = m.getRun("main").getDetPixTOFData( None )

        #add some background to the histogram so we can see its effects
        _addBG( hist )
        #print hist

        #do tbg processing
        #tof indenpendent background is assumed to be at tof  0
        tbgMin, tbgMax = tbgRange(hist)
        from instrument.DetectorMask import DetectorMask
        mask = DetectorMask()

        removeTIBG.reconstruct(tbgMin = tbgMin, tbgMax = tbgMax )
        removeTIBG( hist, mask )
        
        print removeTIBG.bg()
        #check whether timeBG works well
        _check(hist)
        return

    pass # end of TimeBG_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TimeBG_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('vectorCompat.ERebinAllInOne').activate()
##     journal.debug('Rebinner').activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##     journal.debug('TBGProcessor').activate()
##     journal.debug('BGAccumulator').activate()
##     journal.debug('TBGProcessorPerDet').activate()
    journal.info('TBGProcessorPerDet').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
