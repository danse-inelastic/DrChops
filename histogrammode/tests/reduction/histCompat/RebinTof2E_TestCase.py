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


import unittestX as unittest
import journal

from reduction.histCompat.RebinTof2E import RebinTof2E


#helper function to convert tof to energy.
#distance in mm
#tof in mus
from reduction.utils.conversion import v2e
def E(tof, distance): return v2e( distance/tof*1000. )

from histogram import histogram, arange, axis, datasetFromFunction



class RebinTof2E_TestCase(unittest.TestCase):


    def setUp(self):
        #time of flight axis
        tofAxis = self.tofAxis \
                  = axis('tof', arange( 3000., 5000., 50.0, 'd' ),
                         unit = 'microsecond' )
        #I(tof)
        Itof = self.Itof = histogram('Itof', [tofAxis] )
        def I(tof): return 1. + 0.*tof
        Itof[()] = datasetFromFunction( I, [tofAxis] ), \
                   datasetFromFunction( I, [tofAxis] )

        #energy axis 
        self.EAxis = axis( 'energy', arange( 10., 100., 1., 'd' ), unit = 'meV' )

        #distance from moderator to pixel
        self.distance = 10000. #mm
        return

     
    def test(self):
        """RebinTof2E"""
        # a trivial input histogram
        EAxis = self.EAxis
        IE = histogram( 'IE', [EAxis] )

        # rebinner
        distance = self.distance
        from pyre.units.length import mm
        rebinner = RebinTof2E( distance*mm )

        # rebin
        Itof = self.Itof
        rebinner( Itof, IE )

        # check
        print IE
        tofAxis = self.tofAxis
        self.assertAlmostEqual(IE.sum()[0], tofAxis.size() )

        # compare to oracle
        expected = self.oracle()
        print expected

        from pyre.units.time import microsecond
        tofa = tofAxis[1]/microsecond; tofb = tofAxis[-2]/microsecond;
        
        Ea = E(tofa, distance); Eb = E(tofb, distance)
        from pyre.units.energy import meV
        dE = (EAxis[1]-EAxis[0])/meV
        
        for e in arange( Eb, Ea, dE ):
            print  IE[e][0], expected[e][0] 
            self.assertAlmostEqual(
                IE[e][0], expected[e][0], relativeError = 0.01)
            continue
        return


    def test2(self):
        "RebinTof2E: setDistance"
        EAxis = self.EAxis
        IE = histogram( 'IE', [EAxis] )

        from pyre.units.length import mm
        rebinner = RebinTof2E( 0.0*mm )
        distance = self.distance
        rebinner.setDistance( distance*mm )
        Itof = self.Itof
        rebinner( Itof, IE )

        print IE
        tofAxis = self.tofAxis
        self.assertAlmostEqual(IE.sum()[0], tofAxis.size() )

        expected = self.oracle()
        print expected
        
        from pyre.units.time import microsecond
        tofa = tofAxis[1]/microsecond; tofb = tofAxis[-2]/microsecond;
        
        Ea = E(tofa,distance); Eb = E(tofb, distance)
        from pyre.units.energy import meV
        dE = (EAxis[1]-EAxis[0])/meV
        
        for e in arange( Eb, Ea, dE ):
            print  IE[e][0], expected[e][0] 
            self.assertAlmostEqual(
                IE[e][0], expected[e][0], relativeError = 0.01)
            continue
        return
    

    def oracle(self):
        EAxis = self.EAxis
        IE1 = histogram( 'IE', [EAxis] )

        distance = self.distance
        def J(tof): return 2*E(tof, distance)/tof

        tofAxis = self.tofAxis
        Jacobians = histogram( 'Jacobians', [tofAxis] )
        Jacobians[()] = datasetFromFunction( J, [tofAxis] ), None

        def E1(tof): return E(tof, distance)
        from reduction.histCompat.Rebinner import rebinner
        Itof = self.Itof
        rebinner.rebin( Itof, IE1, E1, Jacobians)

        return IE1

    pass # end of RebinTof2E_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(RebinTof2E_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id: RebinTof2E_TestCase.py 1092 2006-08-12 14:12:07Z linjiao $"

# End of file 
