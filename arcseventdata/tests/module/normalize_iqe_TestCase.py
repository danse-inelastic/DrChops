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
class normalize_iqe_TestCase(TestCase):


    def test1(self):
        'calcSolidAngleQE'
        qbegin, qend, qstep = 0, 13, 0.1
        ebegin, eend, estep = -50,50, 1.
        import numpy
        sa = numpy.zeros( 130*100 )
        ei = 70
        npixels = 1024*100

        import arcseventdata.arcseventdata as aa
        pixelPositions = aa.readpixelpositions( 'pixelID2position.bin' )
        
        aa.calcSolidAngleQE_numpyarray(
            qbegin, qend, qstep, ebegin, eend, estep, sa,
            ei, npixels, pixelPositions)
        
        return
    
    pass # end of normalize_iqe_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(normalize_iqe_TestCase)
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
