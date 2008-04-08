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



import unittestX as unittest
import journal

from reduction.histCompat.QRebinner import QRebinner


class QRebinner_TestCase(unittest.TestCase):
     
    def testCtor(self):
        "QRebinner: ctor"
        from pyre.units.energy import meV
        ei = 63 * meV
        from histogram import histogram, arange, axis
        sphiEHist = histogram(
            'S(phi,E)',
            [
            ('phi', arange(100), 'degree' ),
            ('E', arange(-45, 45, 1 ), 'meV'),
            ] )

        QAxis = axis( 'Q', unit = 'angstrom**-1', centers = arange( 0, 13, 0.2 ) )

        rebinner = QRebinner(sphiEHist, ei, QAxis)
        return

    pass 

     
    
def pysuite():
    suite1 = unittest.makeSuite(QRebinner_TestCase)
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
