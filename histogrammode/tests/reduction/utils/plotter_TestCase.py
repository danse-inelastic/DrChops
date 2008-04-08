#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.utils.plotter import defaultPlotter1D, defaultPlotter2D


import unittest


from unittestX import TestCase
class plotter_TestCase(TestCase):

    def test1D(self):
        "pylab plotter: 1D"
        defaultPlotter1D.plot( [1,2,3], [1,2,3] )
        return
        
    def test2D(self):
        "pylab plotter: 2D"
        import numpy
        I = numpy.arange( 0, 12, 1.)
        I.shape = 3,4
        defaultPlotter2D.plot( [1,2,3], [1,2,3,4], I )
        return
    
    pass # end of plotter_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(plotter_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: plotter_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
