#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest
import journal

from reduction.vectorCompat.RebinTof2E import RebinTof2E


class RebinTof2E_TestCase(unittest.TestCase):
     
    def test(self):
        """RebinTof2E"""
        rebinner = RebinTof2E( 10000. )
        
        from numpy import array, arange, ones, zeros, sum
        
        tof = arange( 3000., 5000., 50.0, 'd' )
        Itof = ones( len(tof)-1, 'd' )
        tmpE = zeros( len(tof), 'd' )
        E = arange( 10., 100., 1., 'd' )
        IE = zeros( len(E)-1, 'd' )

        rebinner( tof, Itof, tmpE, E, IE )
        
        self.assertAlmostEqual( sum(IE), tof.size-1 )
        print IE
        return

    pass # end of RebinTof2E_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(RebinTof2E_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: RebinTof2E_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
