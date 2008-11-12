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


from drchops.histCompat.Ipixtof2IpixE import Ipixtof2IpixE

import unittestX as ut


from drchops import units
mm = units.length.mm; cm = units.length.cm; meter = units.length.meter;
meV = units.energy.meV
second = units.time.second


class Ipixtof2IpixE_TestCase(ut.TestCase):

    def test(self):
        "Ipixtof2IpixE"

        mod2sample=7000.*mm; distance = 3000.*mm; 
        ei = 70.*meV; tof0 = mod2sample/( conversion.e2v(ei/meV) *meter/second )
        
        NTOFBINS=1000
        NPIXELS=10#000
        NPHIBINS=100
        NEBINS=100

        from histogram import histogram, axis, arange
        from numpy import ones, zeros
        tofaxis = axis('tof', arange( 3000., 3000. + 100.*(NTOFBINS), 100.0 ),
                       unit = 'microsecond')
        pixelaxis = axis('pixelID', range(NPIXELS) )
        I_pixeltof = histogram( 'I', (pixelaxis, tofaxis) )
        I_pixeltof[(),()] = ones( (NPIXELS, NTOFBINS), 'd' ), ones( (NPIXELS,NTOFBINS), 'd' )

        ef0 = tof2E( tofaxis[0]  - tof0, distance ) * 1.1 #meV
        ef1 = tof2E( tofaxis[-1] - tof0, distance ) * 0.9 #meV
        e1 = ei/meV-ef1
        e0 = ei/meV-ef0
        de = (e1-e0)/NEBINS

        eaxis = axis('energy', arange( e0, e1, de ), unit = "meV")

        dist_pixel = histogram( 'distance', (pixelaxis,), unit='mm' )
        dist_pixel[()] = ones( NPIXELS, 'd' ) * distance,\
                         zeros( NPIXELS, 'd' ) * distance * distance

        print "finished initialization of data, start reduction..."
        
        IpixE = Ipixtof2IpixE(
            I_pixeltof, 
            ei, mod2sample, 
            dist_pixel,
            Eaxis = eaxis)

        print "reduction done."
        print "S=", IpixE
        return
    
    pass # end of Ipixtof2IpixE_TestCase


def tof2E( tof, distance ):
    #tof mus, distance mm
    v = distance/tof
    v /= meter/second
    return conversion.v2e( v )


from reduction.utils import conversion


def pysuite():
    suite1 = ut.makeSuite(Ipixtof2IpixE_TestCase)
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
