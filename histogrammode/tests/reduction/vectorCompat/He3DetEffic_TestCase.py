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


'''
test Functor classes
'''

import unittest
import journal

from reduction.vectorCompat.He3DetEffic import He3DetEffic
from stdVector import vector


class He3DetEffic_TestCase(unittest.TestCase):
     
    def test_ctor(self):
        """He3DetEffic: ctor"""
        de = He3DetEffic( 10.0, 1.27, 450, 5)
        return


    def test_oneenergy(self):
        """He3DetEffic: __call__(energy)"""
        de = He3DetEffic( 10.0, 1.27, 450, 5)
        eff = de( 50.0 )
        self.assertAlmostEqual( eff, 0.8156, 4 )
        return
    

    def test_pressuredeps(self):
        """He3DetEffic: pressure depency of detector efficiency"""
        de10 = He3DetEffic( 10.0, 1.27, 450, 5)
        eff10_50 = de10( 50.0 )
        de6 = He3DetEffic( 6.0, 1.27, 450, 5)
        eff6_50 = de6( 50.0 )
        self.assertAlmostEqual( eff10_50, 0.8156, 4)
        self.assertAlmostEqual( eff6_50, 0.6526, 4 )
        return
    

    pass # end of class


# a simple pure python function to calculate detector efficiency
def efficiency(radius, pressure, E, n=100):
    '''radius: cm
    pressure: atm
    E: meV
    '''
    import numpy as N
    rho = pressure*1.468e20/6
    sig = 5333e-24/1.798*N.sqrt(81.81/E)
    print rho, sig
    x = N.arange(-1,1,2./n)
    y = N.sqrt( 1 - x**2) * radius * 2
    eff = 1.-N.exp(-rho*sig*y)
    return N.average(eff)

    
def pysuite():
    suite1 = unittest.makeSuite(He3DetEffic_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: He3DetEffic_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
