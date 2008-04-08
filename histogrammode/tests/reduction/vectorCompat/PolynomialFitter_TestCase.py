#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittest
import journal

from reduction.vectorCompat.PolynomialFitter import PolynomialFitter
from stdVector import vector

import numpy

class PolynomialFitter_TestCase(unittest.TestCase):
     
    def test1(self):
        """PolynomialFitter: order = 1"""
        x = numpy.arange( 0, 10, 1. )
        y = x 
        fitter = PolynomialFitter( 1 )
        res = fitter.fit(x,y)
        self.assertAlmostEqual( res[0], 0. )
        self.assertAlmostEqual( res[1], 1. )

        x = numpy.arange( 0, 10, 1. )
        y = [1] * 10
        fitter = PolynomialFitter( 1 )
        res = fitter.fit(x,y)

        a0, a1 = res
        
        self.assertAlmostEqual( a0, 1. )
        self.assertAlmostEqual( a1, 0. )
        
        return


    def test2(self):
        """PolynomialFitter: order = 2"""
        x = numpy.arange( 0, 10, 1. )
        y = 3 * x * x + 4*x + 5
        fitter = PolynomialFitter( 2 )
        res = fitter.fit(x,y)
        a0, a1, a2 = res
        
        self.assertAlmostEqual( a0, 5. )
        self.assertAlmostEqual( a1, 4. )
        self.assertAlmostEqual( a2, 3. )
        return

    pass
     
    
def pysuite():
    suite1 = unittest.makeSuite(PolynomialFitter_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: PolynomialFitter_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
