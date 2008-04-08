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



from pyre.applications.Script import Script
from measurement.ins.Fake.Run import Run, integratedCurrent as ic
from measurement.ins.Fake.Measurement import measurement


import unittest


from unittestX import TestCase
class Normalizer_TestCase(TestCase):


    #overide the following two members to create a test case for another Normalizer
    from reduction.pyre.preprocessors.NormalizerUsingIntegratedCurrent import NormalizerUsingIntegratedCurrent as Normalizer
    norm = ic
    

    def test(self):
        """
        """
        testFacility = self


        #create a pyre script to run the test
        class Test(Script):
            
            class Inventory(Script.Inventory):
                import pyre.inventory as inv
                normalizer = inv.facility("normalizer", factory = testFacility.Normalizer)
                pass # end of Inventory

            def main(self):
                run = measurement.getRun("main")
                instrument, g = measurement.getInstrument()
                hist = run.getIdpt()
                
                #keep a copy of original data
                copy = hist.copy()
                
                #call normalizer
                normalizer = self.normalizer
                normalizer.setInput( 'run', run )
                normalizer.setInput( 'histogram', hist )
                hist1 = normalizer.getOutput( 'histogram' )
                testFacility.assertEqual( hist1, hist )

                #compare
                #convert all to 1-D numarray
                normalized = hist.data().storage().asNumarray()*hist.unit()
                normalized.shape = -1,
                copy /= testFacility.norm, 0 #normalize copy
                copy = copy.data().storage().asNumarray() * copy.unit()
                copy.shape = -1,

                #remove unit
                normalized/=hist.unit(); copy/=hist.unit()

                testFacility.assertVectorAlmostEqual( normalized, copy )
                return


            def _defaults(self):
                normalizer = self.inventory.normalizer
                return
            
            def _configure(self):
                si = self.inventory
                self.normalizer = si.normalizer
                return

            pass # end of Test
        t = Test('t')
        t.run()
        return
    

    pass # end of Normalizer_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Normalizer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: NormalizerUsingIntegratedCurrent_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
