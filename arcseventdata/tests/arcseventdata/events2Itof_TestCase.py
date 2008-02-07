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
class events2Itof_TestCase(TestCase):


    def test1(self):
        'events2Itof'
        from  arcseventdata.events2Itof import  events2Itof
        import arcseventdata
        events = arcseventdata.readevents( "events.dat", 10 )
        
        import histogram as H
        tofaxis = H.axis( 'tof', boundaries = H.arange(0, 1000, 10), unit = "microsecond" )
        Itof = H.histogram(
            'I(tof',
            [
            tofaxis,
            ],
            data_type = 'int')
        events2Itof( events, 10, Itof )
        return
    
    pass # end of events2Itof_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Itof_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Itof_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
