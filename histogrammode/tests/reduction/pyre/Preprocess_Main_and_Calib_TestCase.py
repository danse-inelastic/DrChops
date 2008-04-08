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


from reduction.pyre.Preprocess_Main_and_Calib import Preprocess_Main_and_Calib

from pyre.applications.Script import Script

from unittestX import TestCase

class Preprocess_Main_and_Calib_TestCase(TestCase):

    
    def test(self):
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                preprocess = inv.facility(
                    'preprocess', factory = Preprocess_Main_and_Calib )
                
                pass #


            def main(self):
                preprocess = self.inventory.preprocess

                from sampleassembly.predefined.VanadiumPlate import VanadiumPlate
                vSample = VanadiumPlate()

                dataFilename = '../../ins-data/Lrmecs/4849'
                vFilename = '../../ins-data/Lrmecs/4779'
                from measurement.ins.LRMECS import createMeasurement
                measurement = createMeasurement(
                    dataFilename,
                    calibFilename = vFilename,
                    vanadiumSampleAssembly = vSample
                    )

                preprocess.setInput( 'measurement', measurement )
                
                Ei = preprocess.getOutput( 'Ei' )
                Idpt = preprocess.getOutput( 'Idpt' )
                return


            def _defaults(self):
                preprocess = self.inventory.preprocess
                pi = preprocess.inventory
                
                eiSolver = pi.eiSolver
                eiSolver.inventory.monitor1Id = 0
                eiSolver.inventory.monitor2Id = 1

                from reduction.pyre.preprocessors.Step1 import Step1
                pi.preStep1_main = Step1()
                preStep1_main = pi.preStep1_main
                psi = preStep1_main.inventory
                
                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of Preprocess_Main_and_Calib_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Preprocess_Main_and_Calib_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    #journal.info('TBGProcessorPerDet').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
