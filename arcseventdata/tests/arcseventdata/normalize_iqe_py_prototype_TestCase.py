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
class TestCase(TestCase):


    def test1(self):
        'normalize_iqe: calcQ'
        from arcseventdata.normalize_iqe_py_prototype import calcQ

        position = 1, 0, 0
        ei = 70
        e = 70
        q1 = calcQ( position, ei, e )

        position = -1, 0, 0
        ei = 70
        e = 0
        q2 = calcQ( position, ei, e )

        self.assertAlmostEqual( q1*2, q2 )

        from math import sqrt

        position = 0, 1, 0
        ei = 70
        e = 0
        q3 = calcQ( position, ei, e )
        
        self.assertAlmostEqual( q1*sqrt(2), q3 )

        position = 0, 0, 1
        ei = 70
        e = 0
        q3 = calcQ( position, ei, e )
        
        self.assertAlmostEqual( q1*sqrt(2), q3 )
        return


    # this test takes a long time to finish, and the function
    # to test is a prototype implementation in python, and
    # there is c++ implementation already tested in
    # normalize_iqe_TestCase. So this test is not really
    # important
    def _test2(self):
        'normalize_iqe: calcSolidAngleQE'
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        ARCSxml = 'ARCS.xml'
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
                                
        ei = 70
        from histogram import axis, arange
        qaxis = axis( 'Q', arange(0, 13, 0.5), unit = 'angstrom**-1')
        eaxis = axis( 'energy', arange( -50, 50, 5), unit = 'meV' )
        import arcseventdata
        pixelpositions = arcseventdata.readpixelpositions(
            'pixelID2position.bin', npacks, ndetsperpack, npixelsperdet )
        from arcseventdata.normalize_iqe_py_prototype import calcSolidAngleQE
        def mask_function( pixelID ): return 0
        sa = calcSolidAngleQE(
            ei, qaxis, eaxis, pixelpositions, mask_function)

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( sa )
        return
    
    
    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
