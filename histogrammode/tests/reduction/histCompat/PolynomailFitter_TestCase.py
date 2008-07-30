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

from reduction.histCompat.PolynomialFitter import PolynomialFitter


class TestCase(unittest.TestCase):
     

    def test(self):
        import histogram as H
        x = H.axis( 'x', centers = H.arange(10) )
        h = H.histogram( 'h', [x], data = H.arange(10,20,1) )
        a0, a1 = PolynomialFitter(1).fit( h )
        self.assertAlmostEqual( a0, 10 )
        self.assertAlmostEqual( a1, 1 )
        return
    
    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
