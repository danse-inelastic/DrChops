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


from reduction.pyre.preprocessors.TofWindowSelector import TofWindowSelector

from pyre.applications.Script import Script

from unittestX import TestCase
class TofWindowSelector_TestCase(TestCase):

    
    def test(self):
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv

                selectTof = inv.facility(
                    'selectTof', factory = TofWindowSelector )
                
                pass #


            def main(self):
                selectTof = self.inventory.selectTof

                dataFilename = '../../../ins-data/Lrmecs/4849'
                from measurement.ins.LRMECS import createRun
                run = createRun( dataFilename )
                idpt = run.getIdpt()

                selectTof.setInput( 'Idpt', idpt )
                
                print "tofWindow selected = ", selectTof.getOutput( 'tofWindow' )
                return


            def _defaults(self):
                selectTof = self.inventory.selectTof
                si = selectTof.inventory
                return

            pass #
        
        t = Test('t')
        t.run()
        return
    
    pass # end of TofWindowSelector_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TofWindowSelector_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
