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


from reduction.pyre.datasource.LrmecsMeasurement import LrmecsMeasurement
from reduction.pyre.Preprocess_MainDataOnly import Preprocess_MainDataOnly
from reduction.pyre.Idpt2Spe import Idpt2Spe

from pyre.applications.Script import Script
from reduction.pyre.DataStreamModel import DataStreamModel

from unittestX import TestCase
class Combined_TestCase(TestCase):

    
    def testPreprocess_and_Idpt2Spe(self):
        'Preprocess and Idpt2Spe'
        testFacility = self
        
        class Test(Script, DataStreamModel):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                measurementFactory = inv.facility(
                    'measurementFactory', default = LrmecsMeasurement())
                preprocess = inv.facility(
                    'preprocess', default = Preprocess_MainDataOnly() )
                idpt2spe = inv.facility(
                    'idpt2spe', default = Idpt2Spe() )

                connections = inv.list(
                    'connections',
                    default = [
                    'measurementFactory:measurement->measurement:preprocess',
                    'measurementFactory:instrument->instrument:idpt2spe',
                    'preprocess:Idpt->Idpt:idpt2spe',
                    'preprocess:Ei->Ei:idpt2spe',
                    'preprocess:mask->mask:idpt2spe',
                    'idpt2spe:spe->spe:self',
                    ] )
                pass #


            sockets = {
                'in': [],
                'out': ['spe'],
                }


            def __init__(self, name='Test'):
                Script.__init__(self, name)
                DataStreamModel.__init__(self, name, 'PowderReduction' )
                return


            def main(self):
                self._update()
                return


            def _defaults(self):
                preprocess = self.inventory.preprocess
                pi = preprocess.inventory
                
                eiSolver = pi.eiSolver
                eiSolver.inventory.monitor1Id = 0
                eiSolver.inventory.monitor2Id = 1

                from reduction.pyre.preprocessors.Step1 import Step1
                pi.preStep1 = Step1('preStep1')
                preStep1 = pi.preStep1
                psi = preStep1.inventory

                tibgRemover = psi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.

                measurementFactory = self.inventory.measurementFactory
                mi = measurementFactory.inventory
                mi.main = '../../ins-data/Lrmecs/4849'
                mi.interpolateData = True
                return


            def _configure(self):
                Script._configure(self)
                DataStreamModel._configure(self)
                return


            def _init(self):
                Script._init(self)
                DataStreamModel._init(self)
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of Combined_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Combined_TestCase)
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
