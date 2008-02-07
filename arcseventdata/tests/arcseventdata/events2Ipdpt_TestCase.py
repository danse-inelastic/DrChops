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
class events2Ipdpt_TestCase(TestCase):


    def test1(self):
        'events2Ipdpt'
        from  arcseventdata.events2Ipdpt import  events2Ipdpt
        import arcseventdata
        events = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        Ipdpt = H.histogram(
            'I(pack, detector, pixel, tof)',
            [
            ('detectorpackID', range(100)),
            ('detectorID', range(8)),
            ('pixelID', range(128) ),
            ('tof', H.arange(0,1.e-4,1.e-7)),
            ],
            data_type = 'int')
        
        events2Ipdpt( events, 10, Ipdpt, 
                      npacks = 99)
        return
    
    pass # end of events2Ipdpt_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Ipdpt_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Ipdpt_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
