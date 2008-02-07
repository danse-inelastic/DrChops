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
class readevents_TestCase(TestCase):

    def test1(self):
        'readevents'
        import arcseventdata.arcseventdata as aa
        events = aa.readevents( "events.dat", 10 )
        return
    
    def test2(self):
        'readevents'
        import arcseventdata.arcseventdata as aa
        events = aa.readevents( "events.dat", 10, 5 )
        return
    
    pass # end of readevents_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(readevents_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: readevents5A_TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
