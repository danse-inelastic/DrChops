#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.getDetetectorInfo
## Misc. functions regarding detectors.

from histogram import histogram

def getTheoreticalEfficiencis( energy, instrument, detaxes ):
    """ compute detector efficiency according to its geometry and
    the neutron energy. (nothing about experimental data)"""
    from reduction.histCompat.He3DetEffic import He3DetEffic
    class _( DetectorPropertyExtractor):
        def getProperty( self, detector ):
            pressure = detector.pressure()
            radius = detector.shape().radius
            calcor = He3DetEffic(pressure = pressure, radius = radius)
            ret = calcor( energy )
            if ret <= 0.0:
                raise ValueError, "Detector efficiency should be positive: %s" % (
                    ret, )
            return ret
    ret = histogram( 'efficiency', detaxes )
    return _( ret ).render(instrument)


def getScatteringAngles( instrument, geometer, detaxes ):
    '''retrieve scattering angle for each detector'''
    class _( DetectorPropertyExtractor ):
        def getProperty( self, detector ):
            return geometer.scatteringAngle( self.elementSignature() )
    ret = histogram( 'scatteringAngle', detaxes, unit = 'deg' )
    return _(ret).render( instrument )


def getDistances( instrument, geometer, detaxes ):
    class _( DetectorPropertyExtractor ):
        def getProperty( self, detector ):
            return geometer.distanceToSample( self.elementSignature() )
    ret = histogram( 'distance', detaxes, unit = 'meter' )
    return _(ret).render( instrument )


def getPressures( instrument, detaxes ):
    class _( DetectorPropertyExtractor ):
        def getProperty( self, detector ):
            return detector.attributes.pressure
    ret = histogram( 'pressure', detaxes, unit = 'atm' )
    return _(ret).render( instrument )


def getRadii( instrument, detaxes ):
    class _( DetectorPropertyExtractor ):
        def getProperty( self, detector ):
            return detector.shape().radius
    ret = histogram( 'radius', detaxes, unit = 'meter' )
    return _(ret).render( instrument )


from LoopUtils import DetectorVisitor

class DetectorPropertyExtractor( DetectorVisitor ):

    """base class to help extract properties of detectors in a histogram
    """

    def __init__(self, target):
        '''target: the target data object in which the detector property
        will be stored'''
        self._ret = target
        return

    def render(self, instrument, geometer = None):
        ''' render( instrument) --> a histogram of detector properties
        
    - instrument: the instrument to be examined
    - detAxes: a list of detector related axes.
      For example: (detArrayAxis, detPackAxis, detaxes)
        '''
        DetectorVisitor.render(self, instrument, geometer)
        return self._ret


    def onDetector(self, detector):
        detaxis = self._ret.axisFromName('detectorID')
        if detector.id() not in detaxis: return
        prop = self.getProperty( detector )
        self._ret[ self.detectorElementSignature() ] = prop, 0. * prop * prop
        return

    def getProperty(self, detector):
        raise NotImplementedError

    pass # end of P




# version
__id__ = "$Id$"

# End of file 
