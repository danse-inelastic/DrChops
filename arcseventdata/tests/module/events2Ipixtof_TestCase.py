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
class events2Ipixtof_TestCase(TestCase):


    def test1(self):
        'events2Ipixtof'
        import arcseventdata.arcseventdata as aa
        events = aa.readevents( "events.dat", 10 )
        import numpy
        I = numpy.zeros( 100, 'i' )
        
        aa.events2Ipixtof_numpyarray(
            events, 10,
            1024, 1034, 1,
            0, 1.e-5, 1.e-6,
            I)
        return
    
    pass # end of events2Ipixtof_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(events2Ipixtof_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: events2Ipixtof_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
