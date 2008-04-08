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

debug = journal.debug( "VanadiumTransmissionCalculator_TestCase" )
warning = journal.warning( "VanadiumTransmissionCalculator_TestCase" )


from pyre.units.length import cm
from pyre.units.angle import degree
from pyre.units.energy import meV
thickness = 0.2 * cm
width = 6.3 * cm
height = 10. * cm
darkAngle = 135. *degree



class TestCase(unittest.TestCase):

    def test(self):
        "VanadiumTransmissionCalculator: plate"
        from measurement.ins.LRMECS import createRun
        import os
        filename = os.path.join( curdir(),  '..', '..', 'ins-data', 'Lrmecs', '4779' )

        print "loading data file and create instrument and geometer"

        run = createRun( filename )
        instrument, geometer = run.getInstrument()

        print "building sample"
        from sampleassembly.predefined.VanadiumPlate import VanadiumPlate
        vsample = VanadiumPlate( )
        
        print "configuring the calculator"
        from reduction.core.VanadiumTransmissionCalculator import calculator
        calculator.setSampleAssembly( vsample )

        print "computing"
        energy    = 75.0 * meV
        scattering_angle = 45. * degree
        tx = calculator( scattering_angle, energy )

        expected = self.oracle( scattering_angle, energy )

        self.assertAlmostEqual( tx, expected )
        return 


    def oracle(self, angle, energy):
        from reduction.histCompat.VSampleParams import VSampleParams
        params    = VSampleParams( darkAngle, thickness, width )
        from reduction.histCompat.VanPlateTx import VanPlateTx
        calctor   = VanPlateTx(params)

        return calctor( angle, energy )
        
    pass  # end of VanadiumTransmissionCalculator_TestCase


def curdir():
    import os
    global __file__
    return os.path.dirname( __file__ )


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    #from reduction.core.VanadiumTransmissionCalculator import debug
    #debug.activate()

    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
