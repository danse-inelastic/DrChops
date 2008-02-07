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
class events2Idspacing_TestCase(TestCase):


    def test1(self):
        'events2Idspacing'
        import arcseventdata
        from  arcseventdata.events2Idspacing import events2Idspacing
        events = arcseventdata.readevents( "events.dat", 10 )
        pixelPositions = arcseventdata.readpixelpositions( 'pixelID2position.bin' )
        import histogram as H
        daxis = H.axis('d', boundaries = H.arange(0, 4.0, 0.01) )
        h = H.histogram(
            'I(d spacing)',
            [ daxis ],
            data_type = 'int',
            )

        events2Idspacing( events, 10, h, pixelPositions)
        return
    
    pass # end of events2Idspacing_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Idspacing_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Idspacing_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
