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


import drchops.drchops as red

import unittestX as ut


class IpixE2IphiE_TestCase(ut.TestCase):

    def test(self):
        "IpixE2IphiE"

        NPIXELS=10000
        NPHIBINS=100
        NEBINS=100
        
        from numpy import array, arange, ones, zeros, sum
        ebb = arange( -50., -50.+1*(NEBINS+1), 1.0, 'd' )
        IpixE = ones( NEBINS*NPIXELS, 'd' )
        E2pixE = ones( NEBINS*NPIXELS, 'd' )

        phibb = arange( 0, NPHIBINS+1, 1., 'd' )
        
        print "len(ebb)=", len(ebb)
        print "len(phibb)=", len(phibb)

        IphiE = zeros( NPHIBINS*NEBINS, 'd' )
        E2phiE = zeros( NPHIBINS*NEBINS, 'd' )
        saphi = zeros( NPHIBINS, 'd' )
        saE2phi = zeros( NPHIBINS, 'd' )

        phiarr = zeros( NPIXELS, 'd' )
        for i in range( NPIXELS ): phiarr[i] = i%100

        saarr = ones( NPIXELS, 'd' )
        saE2arr = zeros( NPIXELS, 'd' )

        maskarr = zeros( NPIXELS, 'i' )

        print "finished initialization of data, start reduction..."
        red.IpixE2IphiE_numpyarray(
            ebb, IpixE, E2pixE,
            phibb, IphiE, E2phiE, saphi, saE2phi,
            phiarr,
            saarr, saE2arr,
            maskarr)

        print "reduction done."
        print "I(phi,E)=", IphiE
        print "solidangle=", saphi
        return
    
    pass # end of IpixE2IphiE_TestCase



def pysuite():
    suite1 = ut.makeSuite(IpixE2IphiE_TestCase)
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
