#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2005 All Rights Reserved 
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

from reduction.histCompat.VanPlateTx import VanPlateTx
from reduction.histCompat.VSampleParams import VSampleParams

class VanPlateTx_TestCase(unittest.TestCase):
     
    def test(self):
        """VanPlateTx"""
        from pyre.units.angle import degree
        from pyre.units.length import cm
        from pyre.units.energy import meV
        
        darkAngle = 135 * degree
        thickness = 0.2 * cm
        width     = 6.3 * cm
        params    = VSampleParams( darkAngle, thickness, width )
        calctor   = VanPlateTx(params)

        energy    = 75.0 * meV

        for angle in range (180):
            s =  'angle = %s, transmission = %s ' % (angle, calctor( angle*degree, energy))
            print s
            continue
        return
     
    
def pysuite():
    suite1 = unittest.makeSuite(VanPlateTx_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: VanPlateTx_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
