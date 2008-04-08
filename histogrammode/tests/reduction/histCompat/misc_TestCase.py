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

from histogram import *


import unittest
import journal


class misc_TestCase(unittest.TestCase):


    def test_findPeakPosition(self):
        "reduction.histCompat: findPeakPosition"
        x = axis( 'x', arange( -1, 1, 0.1 ) )
        h = histogram( 'h', (x,) )
        def f(x): return x**2
        h[ () ] = datasetFromFunction( f, (x,) ), datasetFromFunction( f, (x,) )
        
        from reduction.histCompat import findPeakPosition
        center = findPeakPosition(h)
        self.assertAlmostEqual( center, 0. )


        def f(x): return (x-0.3)**2
        h[ () ] = datasetFromFunction( f, (x,) ), datasetFromFunction( f, (x,) )
        center = findPeakPosition(h)
        self.assertAlmostEqual( center, 0.3 )
        
        def f(x): return 3*(x-0.15)**2 - 8
        def g(x): return f(x)**2
        h[ () ] = datasetFromFunction( f, (x,) ), datasetFromFunction( g, (x,) )
        center = findPeakPosition(h)
        self.assertAlmostEqual( center, 0.15 )
        return
    
    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(misc_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: misc_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
