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
class mslice_formating_TestCase(TestCase):


    def test1(self):
        'SGrid_str'
        import arcseventdata.arcseventdata as aa
        import numpy
        npixels = 5
        nEbins = 8
        S = numpy.zeros( (npixels, nEbins), 'd' )
        Serr = numpy.zeros( (npixels, nEbins), 'd' )

        s = aa.SGrid_str_numpyarray( S, Serr, npixels, nEbins )
        print s
        return
    
    pass # end of mslice_formating_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(mslice_formating_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: mslice_formating_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
