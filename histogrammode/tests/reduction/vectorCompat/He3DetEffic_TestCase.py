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
