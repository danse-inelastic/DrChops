#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import unittest
import journal


from reduction.vectorCompat.Fit1DFunction import test1, test2, test3


class Fit1DFunction_TestCase(unittest.TestCase):

    def test1(self):
        global test1
        test1()
        return
    
    def test2(self):
        global test2
        test2()
        return
    
    def test3(self):
        global test3
        test3()
        return
    
    pass # end of class
     
    
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
__id__ = "$Id$"

# End of file 
