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


from reduction.histCompat import RebinTof2E_batch as RebinDrivers

import unittestX as ut


from pyre.units.length import mm, meter
from pyre.units.energy import meV
from pyre.units.time import second
from pyre.units.angle import degree


class RebinTof2E_batch_TestCase(ut.TestCase):

    def test_Istartof2IE(self):
        "I(*,tof) --> I(E)"

        distance = 3000.*mm
        
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
        I_pixeltof[(),()] = 1,1#ones( (NPIXELS, NTOFBINS), 'd' ), ones( (NPIXELS,NTOFBINS), 'd' )

        ef0 = tof2E( tofaxis[-1], distance ) * 0.8 #meV
        ef1 = tof2E( tofaxis[0], distance ) * 1.2 #meV
        de = (ef1-ef0)/NEBINS

        eaxis = axis('energy', arange( ef0, ef1, de ), unit = "meV")

        I_E = histogram( 'I(E)', (eaxis,) )
        
        dist_pixel = histogram( 'distance', (pixelaxis,), unit='mm' )
        dist_pixel[()] = distance, 0*distance*distance
        #ones( NPIXELS, 'd' ) * distance,\
        #      zeros( NPIXELS, 'd' ) * distance * distance

        mask_pixel = histogram( 'mask', (pixelaxis,), data_type = 'int' )

        print "finished initialization of data, start reduction..."
        
        RebinDrivers.istartof2IE(
            I_pixeltof, I_E,
            dist_pixel, mask_pixel,
            )

        print "reduction done."
        print "I(E)=", I_E
        return
    
    pass # end of RebinTof2E_batch_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof
    v /= meter/second
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
__id__ = "$Id$"

# End of file 
