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
class events2Ipdpd_TestCase(TestCase):


    def test1(self):
        'events2Ipdpd'
        from  arcseventdata.events2Ipdpd import  events2Ipdpd
        import arcseventdata
        events, nevents = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        Ipdpd = H.histogram(
            'I(pack, detector, pixel, d)',
            [
            ('detectorpackID', range(115)),
            ('detectorID', range(8)),
            ('pixelID', range(128) ),
            ('d spacing', H.arange(0,4,.01)),
            ],
            data_type = 'int')
        
        pixelpositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        
        events2Ipdpd( events, nevents, Ipdpd, pixelpositions)
        return
    
    pass # end of events2Ipdpd_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Ipdpd_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Ipdpd_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
