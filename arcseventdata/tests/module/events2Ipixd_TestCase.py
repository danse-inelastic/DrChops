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
class events2Ipixd_TestCase(TestCase):


    def test1(self):
        'events2Ipixd'
        import arcseventdata.arcseventdata as aa
        nevents = 10
        events = aa.readevents( "events.dat", nevents )
        import numpy
        I = numpy.zeros( 100, 'i' )
        
        pixelPositions = aa.readpixelpositions( 'pixelID2position.bin' )
        
        aa.events2Ipixd_numpyarray(
            events, nevents,
            1024, 1034, 1,
            -50, 50, 10. ,
            I,
            pixelPositions)
        return
    
    pass # end of events2Ipixd_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Ipixd_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Ipixd_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
