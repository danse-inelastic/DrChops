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


import journal


from reduction.interactive import fit1


import unittestX as unittest


class Fit1DFunction_TestCase(unittest.TestCase):


    def test(self):
        """fit1
        """
        from gaussianFunctionWithNoiseToTestFitters import makeGaussianHistogram
        h = makeGaussianHistogram( )
        
        from numpy import exp
        def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

        box = [
            (1000, 50000),
            (-1., 1.),
            (0.5, 1.5),
            ]

        print fit1( h, f, box)
        return
    

    pass # end of Fit1DFunction_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Fit1DFunction_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
##     journal.debug('Fit1DFunction').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Fit1DFunction_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
