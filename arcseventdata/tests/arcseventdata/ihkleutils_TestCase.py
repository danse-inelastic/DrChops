#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest

from unittest import TestCase
class TestCase(TestCase):


    def test1(self):
        from arcseventdata.ihkleutils import tilt

        import histogram as H

        haxis = H.axis('h', H.arange(0,10,2.))
        kaxis = H.axis('k', H.arange(0,10,2.))
        laxis = H.axis('l', H.arange(0,10,2.))
        eaxis = H.axis('energy', H.arange(-50,50,5.))
        axes = [haxis, kaxis, laxis, eaxis]
        
        IhklE = H.histogram('I(h,k,l,E)', axes)


        h1axis = H.axis('h', H.arange(0,10,2.))
        k1axis = H.axis('k', H.arange(0,10,2.))
        l1axis = H.axis('l', H.arange(0,10,2.))
        axes1 = [h1axis, k1axis, l1axis, eaxis]
        IhklE1 = H.histogram('I(h,k,l,E)', axes1)

        tiltmatrix = [
            [1,0,0],
            [0,1,0],
            [0,0,1],
            ]

        tilt(IhklE, IhklE1, tiltmatrix)
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
