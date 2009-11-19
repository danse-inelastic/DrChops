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


from drchops.histCompat.IpixE2IphipsiE import IpixE2IphipsiE

import unittestX as ut


from drchops import units
mm = units.length.mm; cm = units.length.cm; meter = units.length.meter;
meV = units.energy.meV
second = units.time.second


class TestCase(ut.TestCase):

    def test(self):
        "IpixE2IphipsiE"

        import numpy
        
        NPIXELS=10000
        NPHIBINS=100
        NPSIBINS=100
        NEBINS=100
        MINPHI = 0.
        MAXPHI = 135.
        MINPSI = -30.
        MAXPSI = 30.

        from histogram import histogram, axis, arange
        from numpy import ones, zeros
        Eaxis = axis('energy', arange( -50., -50.+1*(NEBINS+1), 1.0, 'd' ), unit = 'meV')
        pixelaxis = axis('pixelID', range(NPIXELS) )
        
        IpixE = histogram( 'I', (pixelaxis, Eaxis) )
        for e in range(-50,50):
            IpixE[(), e] = e, e

        phi_pixel = histogram( 'phi', (pixelaxis,), unit='degree' )
        phi_pixel.I[:] = numpy.arange(MINPHI, MAXPHI-1e-10, (MAXPHI-MINPHI)/NPIXELS)
        phi_pixel.E2[:] = 0

        psi_pixel = histogram( 'psi', (pixelaxis,), unit='degree' )
        psi_pixel.I[:] = numpy.arange(MINPSI, MAXPSI-1e-10, (MAXPSI-MINPSI)/NPIXELS)
        psi_pixel.E2[:] = 0

        sa_pixel = histogram( 'solid angle', (pixelaxis,) )
        sa_pixel[()] = 1,0

        mask_pixel = histogram( 'mask', (pixelaxis,), data_type = 'int' )
        mask_pixel[()] = 0,0

        phiaxis = axis('phi', numpy.arange(MINPHI-5, MAXPHI+5, (MAXPHI-MINPHI+1)/NPHIBINS), unit='degree')
        psiaxis = axis('psi', numpy.arange(MINPSI-5, MAXPSI+5, (MAXPSI-MINPSI+1)/NPSIBINS), unit='degree')


        print "finished initialization of data, start reduction..."
        
        IphipsiE, solidangle_phipsi = IpixE2IphipsiE(
            IpixE, phi_pixel, psi_pixel, sa_pixel, mask_pixel,
            phiaxis = phiaxis, psiaxis = psiaxis)

        print "reduction done."

        for sa in solidangle_phipsi.I.sum(1)[5:-5]:
            # print sa/(1.*NPIXELS/NPHIBINS)
            self.assertAlmostEqual(sa/(1.*NPIXELS/NPHIBINS), 1., 1)
            continue

        for e in [-5,0,13]:
            for i in IphipsiE[(), (), e].I.sum(1)[5:-5]:
                # print i/(1.*NPIXELS/NPHIBINS)
                self.assertAlmostEqual(i/(1.*NPIXELS/NPHIBINS), e, 1)
                continue
            for i in IphipsiE[(), (), e].E2.sum(1)[5:-5]:
                # print i/(1.*NPIXELS/NPHIBINS)
                self.assertAlmostEqual(i/(1.*NPIXELS/NPHIBINS), e, 1)
                continue

        import histogram.plotter as hp
        # hp.defaultPlotter.plot(solidangle_phipsi)
        hp.defaultPlotter.plot(IphipsiE[(),(),1])
        return
    
    pass # end of TestCase



def pysuite():
    suite1 = ut.makeSuite(TestCase)
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
