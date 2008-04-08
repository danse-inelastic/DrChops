#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.vectorCompat.DGTS_RebinTof2E_batch import dgts_RebinTof2E_batch

import unittestX as ut


class DGTS_RebinTof2E_batch_TestCase(ut.TestCase):

    def test(self):
        "DGTS_RebinTof2E_batch"

        mod2sample=7000.; distance = 3000.; radius = 1.27;  pressure = 10.
        ei = 70.; tof0 = mod2sample/conversion.e2v(ei)*1000.;
        
        NTOFBINS=1000
        NPIXELS=10000
        NPHIBINS=100
        NEBINS=100

        from numpy import array, arange, ones, zeros, sum
        tofbb = arange( 3000., 3000. + 100.*(NTOFBINS+1), 100.0, 'd' )
        cntsmat = ones( NTOFBINS*NPIXELS, 'd' )
        err2mat = ones( NTOFBINS*NPIXELS, 'd' )
        tmpEbb = zeros( NTOFBINS+1, 'd' )
        tmpI = zeros( NEBINS, 'd' )

        ef0 = tof2E( tofbb[0]-tof0, distance ) * 1.1;
        ef1 = tof2E( tofbb[-1]-tof0, distance ) * 0.9;
        d_ef = (ef0-ef1)/NEBINS;
        efbb = arange( ef0+d_ef*0.49, ef1-d_ef/2., -d_ef, 'd' )

        ebb = ei - efbb

        print "energy bin boundaries:", ebb

        phibb = arange( 0, NPHIBINS+1, 1., 'd' )
        
        S = zeros( NPHIBINS*NEBINS, 'd' )
        Serr2 = zeros( NPHIBINS*NEBINS, 'd' )
        intsa = zeros( NPHIBINS, 'd' )

        phiarr = zeros( NPIXELS, 'd' )
        for i in range( NPIXELS ): phiarr[i] = i%100

        saarr = ones( NPIXELS, 'd' )

        distarr = ones( NPIXELS, 'd' ) * distance
        radiusarr = ones( NPIXELS, 'd' ) * radius
        pressurearr = ones( NPIXELS, 'd' ) * pressure

        maskarr = zeros( NPIXELS, 'i' )


        from ndarray.NumpyNdArray import arrayFromNumpyArray
        args = [
            tofbb, cntsmat, err2mat, 
            phibb, ebb, S, Serr2, intsa,
            ei, mod2sample, 
            maskarr, phiarr, saarr, distarr,
            radiusarr, pressurearr,
            tmpEbb, tmpI]
        for i, arg in enumerate( args ):
            try:
                arg[0]
                args[i] = arrayFromNumpyArray( arg )
            except:
                pass
            continue
        
        print "finished initialization of data, start reduction..."
        dgts_RebinTof2E_batch( *args )

        print "reduction done."
        print "S=", S
        return
    
    pass # end of DGTS_RebinTof2E_batch_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof * 1000 #m/s
    return conversion.v2e( v )


from reduction.utils import conversion


def pysuite():
    suite1 = ut.makeSuite(DGTS_RebinTof2E_batch_TestCase)
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
__id__ = "$Id: DGTS_RebinTof2E_batch_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
