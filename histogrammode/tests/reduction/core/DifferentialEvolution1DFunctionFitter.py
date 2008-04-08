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



import unittestX as unittest
import journal

debug = journal.debug( "DifferentialEvolution1DFunctionFitter_TestCase" )


from reduction.core.DifferentialEvolution1DFunctionFitter import DifferentialEvolution1DFunctionFitter as Fitter


class DifferentialEvolution1DFunctionFitter_TestCase(unittest.TestCase):
     
    def test1(self):
        "DifferentialEvolution1DFunctionFitter"
        from gaussianFunctionWithNoiseToTestFitters import makeGaussianHistogram
        h = makeGaussianHistogram( )
        
        from numpy import exp
        def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

        box = [
            (1000, 50000),
            (-1., 1.),
            (0.5, 1.5),
            ]

        fit = Fitter()

        print fit( h, f, box)
        
        return 
        
    pass  # end of DifferentialEvolution1DFunctionFitter_TestCase
     
    
def pysuite():
    suite1 = unittest.makeSuite(DifferentialEvolution1DFunctionFitter_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    #from reduction.core.DifferentialEvolution1DFunctionFitter import debug
    #debug.activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
