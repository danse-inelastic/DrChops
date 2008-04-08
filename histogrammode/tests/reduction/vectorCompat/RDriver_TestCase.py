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


'''
test Functor classes
'''

import unittest
import journal

from reduction.vectorCompat.RDriver import RDriver
from stdVector import vector


class RDriver_TestCase(unittest.TestCase):
     
    def test(self):
        """RDriver"""
        #10X10, double array
        spe         = vector(6, 100)
        otherArrLen = 10
        phiBB       = vector(6, 10)
        rdriver     = RDriver( spe, otherArrLen, phiBB )
        norms       = vector(6, 10)
        norms = rdriver.norms()	
        print norms.asList()
        return
     
    
def pysuite():
    suite1 = unittest.makeSuite(RDriver_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: RDriver_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
