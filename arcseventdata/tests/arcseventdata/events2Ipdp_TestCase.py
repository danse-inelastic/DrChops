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
class events2Ipdp_TestCase(TestCase):


    def test1(self):
        'events2Ipdp'
        from  arcseventdata.events2Ipdp import  events2Ipdp
        import arcseventdata
        events, n = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        Ipdp = H.histogram(
            'I(pixelID)',
            [
            ('detectorpackID', range(100)),
            ('detectorID', range(8)),
            ('pixelID', range(128) ),
            ],
            data_type = 'int')
        events2Ipdp( events, n, Ipdp )
        return
    
    pass # end of events2Ipdp_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Ipdp_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Ipdp_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
