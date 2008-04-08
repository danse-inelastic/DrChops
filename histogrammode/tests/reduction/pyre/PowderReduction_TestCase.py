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


from reduction.pyre.PowderReduction import PowderReduction


from unittestX import TestCase
class PowderReduction_TestCase(TestCase):

    
    def test1(self):
        'PowderReduction: LRMECS'
        testFacility = self

        from pyre.applications.Script import Script as base
        class Test(base):

            class Inventory( base.Inventory ):
                import pyre.inventory as inv

                powderReduction = inv.facility(
                    'powderReduction', factory = PowderReduction)
                pass #


            def __init__(self, name='Test'):
                base.__init__(self, name)
                return


            def main(self):
                self.inventory.powderReduction.getOutput( 'sqe' )


            def _defaults(self):
                powderReduction =  self.inventory.powderReduction
                pri = powderReduction.inventory

                SpeReducer = pri.SpeReducer
                Si = SpeReducer.inventory
                
                preprocess = Si.preprocess
                pi = preprocess.inventory
                
                eiSolver = pi.eiSolver
                eiSolver.inventory.monitor1Id = 0
                eiSolver.inventory.monitor2Id = 1

                from reduction.pyre.preprocessors.Step1 import Step1
                pi.preStep1 = Step1()
                preStep1 = pi.preStep1
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                measurementFactory = pri.measurementFactory
                mi = measurementFactory.inventory
                mi.main = '../../ins-data/Lrmecs/4849'
                mi.interpolateData = True
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of PowderReduction_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(PowderReduction_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    #journal.info('TBGProcessorPerDet').activate()
    from reduction.pyre.dsm.Runner import info
    info.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
