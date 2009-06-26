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
        '''combinepixels'''

        ARCSxml = 'ARCS.xml'

        from histogram import axis
        pixelaxis = axis('pixelID', range(1,128,2))
        res = 2
        
        from arcseventdata.combinepixels import combinepixels
        combinepixels(ARCSxml, pixelaxis, 2)
        
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
