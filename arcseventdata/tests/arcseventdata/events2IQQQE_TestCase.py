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
class events2IQQQE_TestCase(TestCase):


    def test1(self):
        'events2IQQQE: integer intensity array'
        from  arcseventdata.events2IQQQE import  events2IQQQE
        import arcseventdata
        events, n = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        IQQQE = H.histogram(
            'I(Qx, Qy, Qz, E)',
            [
            ('Qx', H.arange(-10,10, 1)),
            ('Qy', H.arange(-10,10, 1)),
            ('Qz', H.arange(-10,10, 1)),
            ('energy', H.arange(-50,50,1)),
            ],
            data_type = 'int',
            )
        
        pixelpositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        Ei = 60
        
        events2IQQQE( events, n, IQQQE, Ei, pixelpositions )
        return
    
    def test2(self):
        'events2IQQQE: double intensity array'
        from  arcseventdata.events2IQQQE import  events2IQQQE
        import arcseventdata
        events, n = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        IQQQE = H.histogram(
            'I(Qx, Qy, Qz, E)',
            [
            ('Qx', H.arange(-10,10, 1)),
            ('Qy', H.arange(-10,10, 1)),
            ('Qz', H.arange(-10,10, 1)),
            ('energy', H.arange(-50,50,1)),
            ]
            )
        
        pixelpositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        Ei = 60
        
        events2IQQQE( events, n, IQQQE, Ei, pixelpositions )
        return
    
    pass # end of events2IQQQE_TestCase


def pysuite():
    suite1 = unittest.makeSuite(events2IQQQE_TestCase)
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
