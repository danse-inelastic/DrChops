#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.reduction import *

import unittestX as ut


class RebinTof2E_TestCase(ut.TestCase):

    def test(self):
        "RebinTof2E"
        rebinner = RebinTof2E( 10000.0 )

        from numpy import array, arange, ones, zeros, sum
        tof = arange( 3000., 5000., 50.0, 'd' )
        Itof = ones( len(tof)-1, 'd' )
        tmpE = zeros( len(tof), 'd' )
        E = arange( 10., 100., 1., 'd' )
        IE = zeros( len(E)-1, 'd' )

        RebinTof2E__call__numpyarray( rebinner, tof, Itof, tmpE, E, IE )

        print sum(IE)
        print IE
        return
    
    pass # end of RebinTof2E_TestCase

    
def pysuite():
    suite1 = ut.makeSuite(RebinTof2E_TestCase)
    return ut.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('reduction.Universal1DRebinner').activate()
    journal.debug('reduction.Universal1DRebinner').activate()
    
    pytests = pysuite()
    alltests = ut.TestSuite( (pytests, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: RebinTof2E_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
