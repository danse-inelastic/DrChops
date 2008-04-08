#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
jname = "reduction.core.Idpt2Sqe"
debug = journal.debug( jname )
info = journal.info( jname )
warning = journal.warning( jname )


from AbstractIdpt2Sqe import AbstractIdpt2Sqe


class Idpt2Sqe(AbstractIdpt2Sqe):

    ''' reduce I(det, pix, tof) to S(Q,E) histogram

    I(det, pix, tof) is first reduced to S(phi,E) histogram,
    and then converted to S(Q,E) histogram.
    '''

    parameters = {
        'Idpt2Spe': "reducer to reduce I(det, pix, tof) to S(phi,E)",
        'spe2sqe': 'transformer to transform S(phi,E) to S(Q,E)',
        'phiAxis': "phi axis. instance of histogram.Axis",
        'QAxis': 'Q axis. instance of histogram.Axis',
        'EAxis': 'energy axis. instance of histogram.Axis',
        'mask': "detector mask",
        }
    parameterDocs = '\n  Parameters:\n' 
    parameterDocs += '\n'.join (
        [ "    %s: %s" % (k,v) for k,v in parameters.iteritems() ])
    

    def __init__(self, **kwds):
        """create a reducer to  reduce I(det, pix, tof) to S(Q,E)"""
        import journal

        self.setDefaults( )
        self.set(**kwds)
        return
    __init__.__doc__ += parameterDocs
         


    def setDefaults(self):
        from Idpt2Spe_a import Idpt2Spe_a as Idpt2Spe
        self.Idpt2Spe = Idpt2Spe()
        from Spe2Sqe import spe2sqe
        self.spe2sqe = spe2sqe
        from instrument.DetectorMask import DetectorMask
        self.mask = DetectorMask()

        from histogram import axis, arange
        self.EAxis = axis('energy', arange(-45, 45, 1.), unit='meV')
        self.QAxis = axis('Q', arange(0.0, 13.0, 0.1), unit='1./angstrom')
        self.phiAxis = None
        return


    def set(self, **params):
        for k, v in params.iteritems():
            if k not in self.parameters.iterkeys():
                raise "Cannot set parameter %s to %s: unknown" % (
                    k,v )
            self.__dict__[ k ] = v
            continue
        return


    def __call__(self, ei, Idpt, instrument, geometer, **kwds):
        """__call__(ei, Idpt, instrument, geometer, **params)
  Inputs
    ei: incident energy
    Idpt: I(det, pix, tof) histogram
    instrument: instrument hierarchy
    geometer: geometry information holder
    """
        self.set(**kwds)
        phiAxis = self._phiAxis(
            Idpt.axisFromName( 'detectorID' ), instrument, geometer)
        
        Idpt2Spe =  self.Idpt2Spe
        sphiEHist = Idpt2Spe( ei, Idpt, instrument, geometer,
                              EAxis = self.EAxis, phiAxis = phiAxis)


        sQEHist = self.spe2sqe(ei, sphiEHist, self.QAxis)
        
        return sQEHist
    __call__.__doc__ += parameterDocs


    def _phiAxis(self, detectorIDaxis, instrument, geometer):
        if self.phiAxis is None:
            self.phiAxis = self._create_phiAxis(
                detectorIDaxis, instrument, geometer )
            pass
        return self.phiAxis


    def _create_phiAxis( self, detectorIDaxis, instrument, geometer):
        from getDetectorInfo import getScatteringAngles
        angle_vs_det = getScatteringAngles(
            instrument, geometer, [detectorIDaxis] )
        angles = angle_vs_det.data().storage().asNumarray()

        from numpy import min, max, pi
        phimin = min(angles)
        phimax = max(angles)

        from getDetectorInfo import getRadii, getDistances
        distances = getDistances( instrument, geometer, [detectorIDaxis] )
        aveDist = distances.sum()[0]/distances.size()
        
        radii = getRadii( instrument, [detectorIDaxis] )
        aveRadius = radii.sum()[0]/radii.size()

        dphi = 2*aveRadius/aveDist * 180/pi * 2

        from histogram import axis, arange
        #return axis('phi', arange(0.0, 100.0, 1.0), unit='degree')
        return axis( 'phi', arange(phimin+dphi, phimax, dphi),
                     unit = 'degree' )


    pass # end of Idpt2Sqe


# version
__id__ = "$Id$"

# End of file 
