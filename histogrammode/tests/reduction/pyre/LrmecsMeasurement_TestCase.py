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

from pyre.applications.Script import Script

from unittestX import TestCase
class LrmecsMeasurement_TestCase(TestCase):

    
    def test(self):
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                measurement = inv.facility(
                    'measurement', factory = LrmecsMeasurement )
                
                pass #


            def main(self):
                m = self.inventory.measurement

                measurement = m.getOutput( 'measurement' )
                instrument = m.getOutput( 'instrument' )
                return


            def _defaults(self):
                m = self.inventory.measurement
                m.inventory.main = '../../ins-data/Lrmecs/4849'
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of LrmecsMeasurement_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(LrmecsMeasurement_TestCase)
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
__id__ = "$Id: LrmecsMeasurement_TestCase.py 1298 2007-07-01 23:15:53Z linjiao $"

# End of file 
