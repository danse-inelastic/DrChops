#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittest
import journal

import reduction.histCompat.Fit1DFunction as fit


class Fit1DFunction_TestCase(unittest.TestCase):


    def test1(self):
        fit.test1()
        return
    
    def test3(self):
        fit.test3()
        return
    
    def test4(self):
        fit.test4()
        return
    
    def test5(self):
        fit.test5()
        return
    
    def test6(self):
        fit.test6()
        return
    
    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(Fit1DFunction_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: Fit1DFunction_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
