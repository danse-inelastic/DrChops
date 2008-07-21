#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

from unittest import TestCase
class normalize_iqqqe_TestCase(TestCase):


    def test1(self):
        'calcSolidAngleQQQE'
        qxbegin, qxend, qxstep = -10, 10, 1
        qybegin, qyend, qystep = -10, 10, 1
        qzbegin, qzend, qzstep = -10, 10, 1
        ebegin, eend, estep = -50,50, 10.
        import numpy
        sa = numpy.zeros( 20*20*20*10 )
        ei = 70
        npixels = 1024*100

        import arcseventdata.arcseventdata as aa
        pixelPositions = aa.readpixelpositions( 'pixelID2position.bin' )

        pixel_area = 0.025 * 1./128
        
        aa.calcSolidAngleQQQE_numpyarray(
            qxbegin, qxend, qxstep,
            qybegin, qyend, qystep,
            qzbegin, qzend, qzstep,
            ebegin, eend, estep, sa,
            ei, pixel_area, npixels, pixelPositions)
        
        return
    
    pass # end of normalize_iqqqe_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(normalize_iqqqe_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
