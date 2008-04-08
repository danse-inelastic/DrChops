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


import reduction.reduction as red

import unittestX as ut


class RebinTof2E_batch_TestCase(ut.TestCase):

    def test_Istartof2IE_numpyarray(self):
        "Istartof2IE_numpyarray"

        distance = 3000.
        
        NTOFBINS=1000
        NPIXELS=10000
        NEBINS=100
        
        from numpy import array, arange, ones, zeros, sum
        tofbb = arange( 3000., 3000. + 100.*(NTOFBINS+1), 100.0, 'd' )
        Itof = ones( NTOFBINS*NPIXELS, 'd' )
        Itof_err2 = ones( NTOFBINS*NPIXELS, 'd' )
        tmpEbb = zeros( NTOFBINS+1, 'd' )
        tmpI = zeros( NEBINS, 'd' )

        ef0 = tof2E( tofbb[-1], distance ) * 0.9;
        ef1 = tof2E( tofbb[0], distance ) * 1.1;
        d_ef = (ef1-ef0)/NEBINS;
        efbb = arange( ef0+d_ef*0.49, ef1+d_ef/2., d_ef, 'd' )

        print "len(efbb)=", len(efbb)
        print '# of energy bins=', NEBINS
        
        I_E = zeros( NEBINS, 'd' )
        I_E_err2 = zeros( NEBINS, 'd' )

        distarr = ones( NPIXELS, 'd' ) * distance

        maskarr = zeros( NPIXELS, 'i' )

        print "finished initialization of data, start reduction..."
        
        red.Istartof2IE_numpyarray(
            tofbb, Itof, Itof_err2, 
            efbb, I_E, I_E_err2, 
            distarr, maskarr, 
            tmpEbb, tmpI)

        print "reduction done."
        print "I_E=", I_E
        return
    
    pass # end of RebinTof2E_batch_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof * 1000 #m/s
    return conversion.v2e( v )


from reduction.utils import conversion


def pysuite():
    suite1 = ut.makeSuite(RebinTof2E_batch_TestCase)
    return ut.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('reduction.Universal1DRebinner').activate()
    pytests = pysuite()
    alltests = ut.TestSuite( (pytests, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: RebinTof2E_batch_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
