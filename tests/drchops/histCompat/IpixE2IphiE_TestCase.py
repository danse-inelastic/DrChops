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


from drchops.histCompat.IpixE2IphiE import IpixE2IphiE

import unittestX as ut


from drchops import units
mm = units.length.mm; cm = units.length.cm; meter = units.length.meter;
meV = units.energy.meV
second = units.time.second


class IpixE2IphiE_TestCase(ut.TestCase):

    def test(self):
        "IpixE2IphiE"

        import numpy
        
        NPIXELS=10000
        NPHIBINS=100
        NEBINS=100
        MINPHI = 0.
        MAXPHI = 135.

        from histogram import histogram, axis, arange
        from numpy import ones, zeros
        Eaxis = axis('energy', arange( -50., -50.+1*(NEBINS+1), 1.0, 'd' ), unit = 'meV')
        pixelaxis = axis('pixelID', range(NPIXELS) )
        
        IpixE = histogram( 'I', (pixelaxis, Eaxis) )
        IpixE[(), ()] = 1, 1

        phi_pixel = histogram( 'phi', (pixelaxis,), unit='degree' )
        phi_pixel.I[:] = numpy.arange(MINPHI, MAXPHI, (MAXPHI-MINPHI)/NPIXELS)
        phi_pixel.E2[:] = 0

        sa_pixel = histogram( 'solid angle', (pixelaxis,) )
        sa_pixel[()] = 1,0

        mask_pixel = histogram( 'mask', (pixelaxis,), data_type = 'int' )
        mask_pixel[()] = 0,0

        phiaxis = axis('phi', numpy.arange(MINPHI, MAXPHI+1, (MAXPHI-MINPHI+1)/NPHIBINS), unit='degree')

        #print 'phiaxis=', phiaxis
        #print 'phi_pixel=', phi_pixel

        print "finished initialization of data, start reduction..."
        
        IphiE, solidangle_phi = IpixE2IphiE(
            IpixE,
            phi_pixel, sa_pixel, mask_pixel,
            phiaxis = phiaxis)

        print "reduction done."
        #print "I(phi,E)=", IphiE
        print "solidangle(phi)=", solidangle_phi
        for sa in solidangle_phi.I:
            self.assertAlmostEqual(sa/(1.*NPIXELS/NPHIBINS), 1., 1)
            continue
        return
    
    pass # end of IpixE2IphiE_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof
    v /= meter/second
    return conversion.v2e( v )


from reduction.utils import conversion


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
