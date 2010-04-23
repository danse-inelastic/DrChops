#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import arcseventdata, math

import unittest

from unittest import TestCase
class TestCase(TestCase):


    def test1(self):
        'ParallelHistogrammer.partition'
        from arcseventdata.parallel_histogrammers.ParallelHistogrammer import partition

        datafile = 'ARCS_180_neutron_event.dat'
        files = [datafile for i in range(2) ]
        N = arcseventdata.getnumberofevents(datafile)

        p1 = partition(files, 1)
        self.assertEqual(len(p1), 1)
        p10 = p1[0]
        self.assertEqual(len(p10), 2)
        self.assertEqual(p10.nevents, 2*N)

        p2 = partition(files, 2)
        self.assertEqual(len(p2), 2)
        p20 = p2[0]
        self.assertEqual(len(p20), 1)
        self.assertEqual(p20.nevents, N)
        
        p3 = partition(files, 3)
        self.assertEqual(len(p3), 3)
        p30 = p3[0]
        self.assertEqual(len(p30), 1)
        self.assertEqual(p30.nevents, int(math.ceil(2.*N/3)))
        
        p31 = p3[1]
        self.assertEqual(len(p31), 2)
        self.assertEqual(p31.nevents, int(math.ceil(2.*N/3)))
        n = p31[0].size
        self.assertEqual(n, N-int(math.ceil(2.*N/3)))
        
        p32 = p3[2]
        self.assertEqual(len(p32), 1)
        self.assertEqual(p32.nevents, 2*N-2*int(math.ceil(2.*N/3)))

        return
    
        
    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
