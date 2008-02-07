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
class histogramFrom2colascii_TestCase(TestCase):


    def test1(self):
        'histogramFrom2colascii'
        from arcseventdata.histogramFrom2colascii import convert
        h = convert('itof.dat')
        print h
        return
    
    pass # end of histogramFrom2colascii_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(histogramFrom2colascii_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: histogramFrom2colascii_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
