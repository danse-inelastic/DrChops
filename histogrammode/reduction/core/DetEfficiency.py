#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.core.DetEfficiency
## compute detector efficiency given a detector


from histogram import histogram
from pyre.units.pressure import atm
from pyre.units.length import mm



class DetEfficiency:

    def __init__(self):
        self._cache = {}
        return


    def efficiency_vs_energy(self, detector, energyAxis):
        "return histogram eff(energy)"
        cache = self._cache
        key = self._key(detector, energyAxis)
        result = cache.get( key )
        if result:
            return result

        calculator = Calculator(detector)
        result = cache[ key ] = calculator( energyAxis )
        
        return result


    def _key(self, detector, energyAxis):
        #to speed up, we implement a caching mechanism
        #many detectors might have similar properties such as length, radius, and pressure
        #so we can reuse some computations
        radius = detector.shape().radius/mm
        pressure = detector.attributes.pressure/atm
        return radius, pressure, id(energyAxis)

    pass # end of DetEfficiency


#implementation class
class Calculator:

    '''Calculator implementation class. not for public use
    '''
    
    def __init__(self,
                 detector,
                 nPoints=500,
                 dtype=6,
                 engine = None ):
        """Create a calculator of detector efficiency for a detector
        
          - detector: instrument.elements.LPSD instance 
        """
        # this is very bad. should go into the instrument package
        pressure = detector.attributes.pressure
        radius = detector.shape().radius
        
        if engine is None:
            from reduction.histCompat.He3DetEffic import He3DetEffic
            engine = He3DetEffic( pressure = pressure, radius = radius,
                                  nPoints = nPoints, dtype = dtype )
        self._engine = engine
        return


    def __call__(self, energyAxis):
        """calculate efficiency histograms"""
        res = self._makeDetEfficHist( energyAxis )
        return res


    def _makeDetEfficHist( self, energyAxis):
        from histogram.Axis import Axis
        assert isinstance(energyAxis, Axis), "%s is not an axis" %(
            energyAxis, )
        from histogram import histogram
        detEfficHist = histogram(
            "detector-efficiency", (energyAxis,), unit = '1' )
        
        efficCalcor = self._engine
        efficCalcor( energyAxis, detEfficHist )
        
        return detEfficHist

    pass




##-----------obsolete--------------------------------------------------------
def _findOneDetector( instrument ):
    
    from reduction.LoopUtils import DetectorVisitor
    
    class Finder(DetectorVisitor):

        def render(self, instrument, geometer = None):
            self.found = None
            DetectorVisitor.render(self, instrument, geometer )
            return self.found
        

        def onDetector(self, detector):
            self.found = detector
            return


        def onElementContainer(self, container):
            if self.found: return
            return DetectorVisitor.onElementContainer( self, container )

        pass # end of Finder

    finder = Finder( )
    
    return finder.render( instrument )
##-----------obsolete--------------------------------------------------------



# version
__id__ = "$Id: DetEfficiency.py 1208 2006-11-19 07:54:11Z linjiao $"

# End of file 
