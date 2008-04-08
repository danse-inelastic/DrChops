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


import unittest


from reduction.pyre.Preprocess_MainDataOnly import Preprocess_MainDataOnly
from reduction.pyre.Preprocess_All import Preprocess_All
from reduction.pyre.preprocessors.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks
from reduction.pyre.Idpt2Spe import Idpt2Spe
from reduction.pyre.SpeReducer import SpeReducer



from pyre.applications.Script import Script as base
class Test(base):

    class Inventory( base.Inventory ):
        import pyre.inventory as inv

        speReducer = inv.facility('speReducer', default = SpeReducer ())
        pass #


    def __init__(self, name='Test'):
        base.__init__(self, name)
        return




from unittestX import TestCase
class SpeReducer_TestCase(TestCase):

    
    def _test1(self):
        'SpeReducer: LRMECS, all'
        
        testFacility = self
        
        class Test1(Test):


            def main(self):
                from sampleassembly.predefined.VanadiumPlate import VanadiumPlate
                vSample = VanadiumPlate()

                dataFilename = '../../ins-data/Lrmecs/4849'
                mtFilename = '../../ins-data/Lrmecs/4844'
                vFilename = '../../ins-data/Lrmecs/4779'
                from measurement.ins.LRMECS import createMeasurement
                measurement = createMeasurement(
                    dataFilename,
                    calibFilename = vFilename,
                    mtFilename = mtFilename,
                    vanadiumSampleAssembly = vSample
                    )

                speReducer = self.inventory.speReducer
                speReducer.setInput( 'measurement', measurement )
                spe = speReducer.getOutput( 'spe' )
                return
                

            def _defaults(self):
                speReducer = self.inventory.speReducer
                si = speReducer.inventory

                si.preprocess = Preprocess_All()

                preprocess = si.preprocess
                pi = preprocess.inventory
                
                eiSolver = pi.eiSolver
                eiSolver.inventory.monitor1Id = 0
                eiSolver.inventory.monitor2Id = 1

                preStep1 = pi.preStep1_main
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                preStep1 = pi.preStep1_mt
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.
                return

            pass #
        
        t = Test1('t')
        t.run()
        return
    

    def test2(self):
        'SpeReducer: LRMECS, main data only'
        testFacility = self
        
        class Test2(Test):

            def main(self):
                dataFilename = '../../ins-data/Lrmecs/4849'
                from measurement.ins.LRMECS import createMeasurement
                measurement = createMeasurement(dataFilename)

                speReducer = self.inventory.speReducer
                speReducer.setInput( 'measurement', measurement )
                spe = speReducer.getOutput( 'spe' )
                return


            def _configure(self):
                speReducer = self.inventory.speReducer
                si = speReducer.inventory

                si.preprocess = Preprocess_MainDataOnly()
                si.configureComponents()

                preprocess = si.preprocess
                pi = preprocess.inventory
                
                eiSolver = pi.eiSolver
                eiSolver.inventory.monitor1Id = 0
                eiSolver.inventory.monitor2Id = 1

                preStep1 = pi.preStep1
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                Test._configure(self)
                return

            pass #
        
        t = Test2('t')
        t.run()
        return
    
    def _test3(self):
        'SpeReducer: PHAROS, all'
        
        testFacility = self

        from reduction.pyre.preprocessors.Step1 import Step1 as base
        class Step1(base):

            def _defaults(self):
                base._defaults(self)
                from reduction.pyre.preprocessors.NormalizerUsingIntegratedCurrent import NormalizerUsingIntegratedCurrent as N
                self.inventory.normalizer = N()
                return
            pass # end of Step1
        
        class Test1(Test):

            def main(self):
                main = '../../ins-data/Pharos/Pharos_342.nx.h5'
                mt = '../../ins-data/Pharos/Pharos_351.nx.h5'
                calib = '../../ins-data/Pharos/Pharos_318.nx.h5'
                instrumentFilename = "../../ins-data/Pharos/PharosDefinitions.txt"

                from sampleassembly.predefined.VanadiumPlate import VanadiumPlate
                vSample = VanadiumPlate()

                from measurement.ins.Pharos import createMeasurement
                measurement = createMeasurement(
                    instrumentFilename, main, calib, mt,
                    vanadiumSampleAssembly = vSample)

                speReducer = self.inventory.speReducer
                speReducer.setInput( 'measurement', measurement )
                spe = speReducer.getOutput( 'spe' )
                return


            def _defaults(self):
                speReducer = self.inventory.speReducer
                si = speReducer.inventory

                si.preprocess = Preprocess_All()

                preprocess = si.preprocess
                pi = preprocess.inventory

                pi.eiSolver = IncidentEnergySolver_UseElasticPeaks()
                eiSolver = pi.eiSolver

                pi.preStep1_main = Step1()
                preStep1 = pi.preStep1_main
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                pi.preStep1_mt = Step1()
                preStep1 = pi.preStep1_mt
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                return

            pass #
        
        t = Test1('t')
        t.run()
        return
    

    pass # end of SpeReducer_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(SpeReducer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    #journal.info('TBGProcessorPerDet').activate()
    from reduction.pyre.dsm.Runner import info
    info.activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    import os
    print os.times()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id: SpeReducer_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
