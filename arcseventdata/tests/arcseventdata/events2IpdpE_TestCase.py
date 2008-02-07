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
class events2IpdpE_TestCase(TestCase):


    def test1(self):
        'events2IpdpE'
        from  arcseventdata.events2IpdpE import  events2IpdpE
        import arcseventdata
        events = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        IpdpE = H.histogram(
            'I(pack, detector, pixel, E)',
            [
            ('detectorpackID', range(100)),
            ('detectorID', range(8)),
            ('pixelID', range(128) ),
            ('energy', H.arange(-50,50,1)),
            ],
            data_type = 'int')
        
        pixelpositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        Ei = 60
        
        events2IpdpE( events, 10, IpdpE, Ei, pixelpositions,
                      npacks = 99)
        return
    
    pass # end of events2IpdpE_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2IpdpE_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2IpdpE_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
