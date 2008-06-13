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

from pyre.units.pressure import atm
from pyre.units.length import mm
from pyre.units.energy import meV


import unittestX as unittest
import journal

from reduction.core.DetEfficiency import DetEfficiency as DetEfficiency

#dummy instrument
#you can see the requirements of instrument and detector interfaces
class Attributes: pass
class Tube:
    def __init__(self, radius, height ):
        self.radius = radius
        self.height = height
        return
    pass
class Detector:
    def __init__(self):
        attributes = Attributes()
        attributes.pressure = 10.*atm
        self._shape = Tube( 12.5*mm, 1000.*mm )
        self.attributes = attributes
        return
    def shape(self): return self._shape
    def identify(self, visitor): return visitor.onDetector(self)
    def id(self): return 0
    pass # end of Detector
detector = Detector()

class Instrument:
    def elements(self):
        return self._elements
    def identify(self, visitor): return visitor.onInstrument(self)
    pass # end of Instrument
instrument = Instrument()
instrument._elements = [ detector ]


class DetEfficiency_TestCase(unittest.TestCase):
     
    def testCtor(self):
        "DetEfficiency: ctor"
        detector_efficiency = DetEfficiency()
        return


    def testCalcEfficHist(self):
        "DetEfficiency: calcEfficHist"
        detector_efficiency = DetEfficiency( )

        from histogram import axis, arange
        EAxis = axis( 'energy', arange(-50, 50, 1.), 'meV' )
        Ei = 60. * meV
        EfAxis = -EAxis + Ei
        efficHist = detector_efficiency.efficiency_vs_energy( detector, EfAxis )
        
        from histogram.plotter import defaultPlotter
        defaultPlotter.interactive( False )
        defaultPlotter.plot( efficHist )
        return


    def testCache(self):
        "DetEfficiency: cache mechansim"
        detector_efficiency = DetEfficiency( )

        from histogram import axis, arange
        EAxis = axis( 'energy', arange(-50, 50, 1.), 'meV' )
        Ei = 60. *meV
        EfAxis = -EAxis + Ei
        efficHist = detector_efficiency.efficiency_vs_energy( detector, EfAxis )
        
        efficHist1 = detector_efficiency.efficiency_vs_energy( detector, EfAxis )
        self.assert_( efficHist1 is efficHist )
        return

    pass 
     
    
def pysuite():
    suite1 = unittest.makeSuite(DetEfficiency_TestCase)
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
