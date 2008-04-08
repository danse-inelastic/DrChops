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


from reduction.pyre.preprocessors.Step1 import Step1

from pyre.applications.Script import Script

from unittestX import TestCase
class Step1_TestCase(TestCase):

    
    def test(self):
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                preprocess = inv.facility(
                    'preprocess', factory = Step1 )
                
                pass #


            def main(self):
                preprocess = self.inventory.preprocess

                dataFilename = '../../../ins-data/Lrmecs/4849'
                from measurement.ins.LRMECS import createRun
                run = createRun( dataFilename )

                from instrument import mask
                mask = mask()

                preprocess.setInput( 'run', run )
                preprocess.setInput( 'mask', mask )
                
                print preprocess.getOutput( 'Idpt' )
                return


            def _defaults(self):
                preprocess = self.inventory.preprocess
                pi = preprocess.inventory
                
                tibgRemover = pi.tibgRemover
                tibgRemover.inventory.tbgMin = 5000.
                tibgRemover.inventory.tbgMax = 5500.
                
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of Step1_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Step1_TestCase)
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
