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


from reduction.histCompat.DGTS_RebinTof2E_batch import dgts_RebinTof2E_batch

import unittestX as ut


from pyre.units.length import mm, meter, cm
from pyre.units.pressure import atm
from pyre.units.energy import meV
from pyre.units.time import second
from pyre.units.angle import degree


class DGTS_RebinTof2E_batch_TestCase(ut.TestCase):

    def test(self):
        "DGTS_RebinTof2E_batch"

        mod2sample=7000.*mm; distance = 3000.*mm; radius = 1.27*cm;  pressure = 10.*atm
        ei = 70.*meV; tof0 = mod2sample/( conversion.e2v(ei/meV) *meter/second )
        
        NTOFBINS=1000
        NPIXELS=10000
        NPHIBINS=100
        NEBINS=100

        from histogram import histogram, axis, arange
        from numpy import ones, zeros
        tofaxis = axis('tof', arange( 3000., 3000. + 100.*(NTOFBINS), 100.0 ),
                       unit = 'microsecond')
        pixelaxis = axis('pixel', range(NPIXELS) )
        I_pixeltof = histogram( 'I', (pixelaxis, tofaxis) )
        I_pixeltof[(),()] = ones( (NPIXELS, NTOFBINS), 'd' ), ones( (NPIXELS,NTOFBINS), 'd' )

        ef0 = tof2E( tofaxis[0]  - tof0, distance ) * 1.1 #meV
        ef1 = tof2E( tofaxis[-1] - tof0, distance ) * 0.9 #meV
        e1 = ei/meV-ef1
        e0 = ei/meV-ef0
        de = (e1-e0)/NEBINS

        eaxis = axis('energy', arange( e0, e1, de ), unit = "meV")
        phiaxis = axis('phi', arange( NPHIBINS ) )

        S_pe = histogram( 'S', (phiaxis, eaxis) )
        sa_p = histogram( 'solid angle', (phiaxis,) )
        
        phi_pixel = histogram( 'phi', (pixelaxis,), unit = 'deg' )
        #print phi_pixel.dimension() == 1
        for i in range( NPIXELS ): phi_pixel[i] = i%100 * degree, 0 * degree
        sa_pixel = histogram( 'solid angle', (pixelaxis,) )
        sa_pixel[()] = ones( NPIXELS, 'd' ), None

        dist_pixel = histogram( 'distance', (pixelaxis,), unit='mm' )
        dist_pixel[()] = ones( NPIXELS, 'd' ) * distance,\
                         zeros( NPIXELS, 'd' ) * distance * distance

        radius_pixel = histogram( 'radius', (pixelaxis,), unit='cm' )
        radius_pixel[()] = ones( NPIXELS, 'd' ) * radius,\
                           zeros( NPIXELS, 'd' ) * radius * radius

        pressure_pixel = histogram( 'pressure', (pixelaxis,), unit='atm' )
        pressure_pixel[()] = ones( NPIXELS, 'd' ) * pressure,\
                             zeros( NPIXELS, 'd' ) * pressure * pressure

        mask_pixel = histogram( 'mask', (pixelaxis,), data_type = 'int' )

        print "finished initialization of data, start reduction..."
        
        dgts_RebinTof2E_batch(
            I_pixeltof, S_pe, sa_p,
            ei, mod2sample, 
            mask_pixel, phi_pixel, sa_pixel, dist_pixel,
            radius_pixel, pressure_pixel)

        print "reduction done."
        print "S=", S_pe
        print "solid angle=", sa_p
        return
    
    pass # end of DGTS_RebinTof2E_batch_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof
    v /= meter/second
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
