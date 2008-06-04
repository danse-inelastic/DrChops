#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittestX as unittest
import journal

from reduction.histCompat.He3DetEffic import He3DetEffic


class He3DetEffic_TestCase(unittest.TestCase):
     
    def testCtor(self):
        "He3DetEffic: ctor"
        calculator = He3DetEffic(
            pressure = "10.0*atm", radius ="2.5*cm",
            nPoints=500, dtype=6, engine_factory = None)
        calculator = He3DetEffic(
            pressure = "10.0*atm", radius ="2.5*cm",
            costheta = 0.8,
            nPoints=500, dtype=6, engine_factory = None)
        return


    def test__call__(self):
        "He3DetEffic: __call__"
        calculator = He3DetEffic(
            pressure = "10.0*atm", radius = "2.5*cm",
            nPoints=500, dtype=6, engine_factory = None)

        #call single energy value
        from pyre.units.energy import meV
        calculator( 60 * meV )

        #call with an energy axis
        from histogram import axis, arange, histogram
        efAxis = axis( 'ef', arange( 10, 110., 1. ), unit='meV' )
        detEfficHist = histogram(
            'detEffic', [efAxis], unit = '1' )

        calculator( efAxis, detEfficHist )

        from histogram.plotter import defaultPlotter
        defaultPlotter.interactive( False )
        defaultPlotter.plot( detEfficHist )
        return


    def test__call__2(self):
        "He3DetEffic: __call__( ..., costheta = ...)"
        calculator = He3DetEffic(
            pressure = "10.0*atm", radius = "2.5*cm",
            nPoints=500, costheta = 0.8,
            dtype=6, engine_factory = None)

        #call single energy value
        from pyre.units.energy import meV
        calculator( 60 * meV )

        #call with an energy axis
        from histogram import axis, arange, histogram
        efAxis = axis( 'ef', arange( 10, 110., 1. ), unit='meV' )
        detEfficHist = histogram(
            'detEffic', [efAxis], unit = '1' )

        calculator( efAxis, detEfficHist )

        from histogram.plotter import defaultPlotter
        defaultPlotter.interactive( False )
        defaultPlotter.plot( detEfficHist )
        return

    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(He3DetEffic_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
