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
import journal

from reduction.histCompat.Normalizer import Normalizer


class Normalizer_TestCase(unittest.TestCase):
     
    def testCtor(self):
        "Normalizer: ctor"
        n = Normalizer( 10.0, 10.0 )
        return


    def testNormalize(self):
        "Normalizer: normalize"
        n = Normalizer( 10.0, 1.0 )
        from histogram import makeHistogram
        name = "h"
        axes = [ ('t', [1,2,3], 'second') ]
        data = [1.,2.,3.]
        errs = [0.,0.,0.]
        h = makeHistogram( name, axes, data, errs )
        n.normalize( h )
        self.assertAlmostEqual( h[ 1 ][0], 0.1 )
        self.assertAlmostEqual( h[ 1 ][1], 0.0001 )
        return
    
    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(Normalizer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: Normalizer_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
