#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005-2008 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import drchops.drchops as binding

import unittestX as ut


class Itof2IE_batch_TestCase(ut.TestCase):

    def test_Itof2IE_batch_numpyarray(self):
        "Itof2IE_batch_numpyarray"

        distance = 3000.
        
        NTOFBINS=1000
        NPIXELS=10
        NEBINS=100
        
        from numpy import array, arange, ones, zeros, sum
        tofbb = arange( 3000., 3000. + 100.*(NTOFBINS+1), 100.0, 'd' )
        Itof = ones( NTOFBINS*NPIXELS, 'd' )
        Itof_err2 = ones( NTOFBINS*NPIXELS, 'd' )
        tmpEbb = zeros( NTOFBINS+1, 'd' )

        ei = 60; mod2sample = 0
        
        ef0 = tof2E( tofbb[-1], distance ) * 0.9;
        ef1 = tof2E( tofbb[0], distance ) * 1.1;
        e0 = 60-ef1
        e1 = 60-ef0
        d_e = (e1-e0)/NEBINS;
        ebb = arange( e0+d_e*0.49, e1+d_e/2., d_e, 'd' )

        print "len(ebb)=", len(ebb)
        print '# of energy bins=', NEBINS
        
        I_E = zeros( NPIXELS*NEBINS, 'd' )
        I_E_err2 = zeros( NPIXELS*NEBINS, 'd' )
        
        distarr = ones( NPIXELS, 'd' ) * distance

        print "finished initialization of data, start reduction..."

        binding.Itof2IE_batch_numpyarray(
            tofbb, Itof, Itof_err2, 
            ebb, I_E, I_E_err2,
            ei, mod2sample,
            distarr, 
            tmpEbb,
            )

        print "reduction done."
        print "I_E=", I_E
        return
    
    pass # end of Itof2IE_batch_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof * 1000 #m/s
    return conversion.v2e( v )


from reduction.utils import conversion


def pysuite():
    suite1 = ut.makeSuite(Itof2IE_batch_TestCase)
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
__id__ = "$Id$"

# End of file 
