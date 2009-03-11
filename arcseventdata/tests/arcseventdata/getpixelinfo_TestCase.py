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
        '''getpixelinfo'''

        ARCSxml = 'ARCS.xml'
        
        import arcseventdata as aed
        infos = aed.getinstrumentinfo(ARCSxml)

        positions = infos['pixelID-position mapping array']
        detaxes = infos['detector axes']

        from instrument.nixml import parse_file
        instrument = parse_file( ARCSxml )
        
        from arcseventdata.getpixelinfo import getpixelinfo
        histograms = getpixelinfo(positions, detaxes, instrument)
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
