#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                                 Max Kresch
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



## \package reduction.core.IncidentEnergySolver_UseElasticPeaks
## The solver in this package
## converts I(*,tof) to I(E) and the position of the peak
## in the obtained I(E) curve is regarded as the neutron incident
## energy.
##
## ##########################
## older implementation:
## Incident energy solver originally written by Max.
##
## It collects counts in all
## pixels with similar distance from sample, and add them together.
## Then a function
## is fit to each counts-vs-tof curves, in order to find out the velocity
## (and energy) of the incident neutron.


import journal
jrnltag = 'IncidentEnergySolver_UseElasticPeaks' 
debug = journal.debug(jrnltag)
info = journal.info(jrnltag)


from AbstractIncidentEnergySolver import AbstractIncidentEnergySolver as _base
from ParallelComponent import ParallelComponent

from pyre.units.energy import meV


class IncidentEnergySolver_UseElasticPeaks(_base, ParallelComponent):
    

    """This soliver converts I(tof) of each pixel to I(E), and add them
    all together. The obtained I(E) should have a peak. The peak position
    is regarded as the neutron incident energy.

    The conversion from I(tof) to I(E) is straightforward.
    The neutron energy, E, is calculated by first computing the velocity
    as

      v = L/tof

    where L is the distance between the pixel and the source. And then the
    velocity is easily converted to neutron energy.

    """

    def __init__(self, numPoints = 8, Eaxis = (20*meV, 200*meV, 0.5*meV),
                 detectorSlice = None):
        '''__init__( numPoints = 8 )

        create new Ei solver, which makes use of elastic peaks.

        numPoints: number of sampling points around the elastic peak
          at a I(tof) curve.
        Eaxis: a tuple of (Emin, Emax, dE) to create an axis of neutron energy
          on which the I(E) histogram will be obtained. This I(E) curve should
          show a peak, and the position of that peak is the neutron energy
          will want to compute.
        detectorSlice: It is usually not necessary to use all pixels to
          compute incident neutron energy. Thousands of pixels should be
          pretty good. If you provide detectorSlice argument, a portion of
          the I(*,tof) histogram will be used.
          For example, suppose a detector system has 200 detectors. and each
          detector has 40 pixels. And we want to use the first 25 detectors,
          and all 40 pixels of those 25 detectors, then

            detectorSlice = (0,25), ()

          By default, detectorSlice=None and no slicing will be done.
            
        '''
        self.numPoints = numPoints

        from numpy import array
        Emin, Emax, dE = array(Eaxis)/meV

        from histogram import axis, arange
        self.Eaxis = axis( 'energy', arange(Emin, Emax, dE), unit = 'meV' )

        self.detectorSlice = detectorSlice
        return


    def __call__(self, run = None, mask=None, idpt = None):
        '''__call__( run, mask = None)

        solve Ei for an experimental run.

        inputs:

          - run: an experimental run. instance of measurement.Run. I(*detectorlayers, tof) are read from this instance.
          - mask: a detector mask. None means no mask
          - idpt: I(*detectorlayers, tof) histogram. If this is supplied, the parameter "run" is ignored
        '''
        if not self.parallel or self.mpiRank == 0:
            ei = self.__call__1(run = run, mask = mask, idpt = idpt)
            pass
        
        if self.parallel:
            #send result to all nodes
            channel = 99998
            if self.mpiRank == 0:
                for i in range(1, self.mpiSize):
                    self.mpiSend( ei, i, channel )
                    continue
                pass
            else:
                ei = self.mpiReceive( 0, channel )
                pass
            pass # endif self.parallel
        return ei


    def __call__1(self, run = None, mask = None, idpt = None):
        '''__call__( run, mask = None)

        solve Ei for an experimental run.

        inputs:

          - run: an experimental run. instance of measurement.Run
          - mask: a detector mask. None means no mask
        '''
        numPoints = self.numPoints
        instrument, geometer = run.getInstrument()

        if mask is None:
            from instrument.DetectorMask import DetectorMask
            mask = DetectorMask()
            pass
        
        if idpt is None:
            idpt = self._readIdpt(run)

        axes = idpt.axes()
        detaxes = axes[:-1]

        from getPixelInfo import getPixelGeometricInfo
        phis, solid_angles, distances, radiuss, pressures = \
              getPixelGeometricInfo(instrument, geometer, detaxes )

        #we need distance from moderator to pixel, instead of
        #distance from sample to pixel
        distances = distances.copy() # we must use a copy, otherwise it will contaminate the original data
        mod2sample = geometer.distanceToSample( instrument.getModerator() )
        distances += mod2sample, mod2sample*mod2sample*0.0
        
        #mask
        from mask import maskMatrix
        mask = maskMatrix( mask, detaxes )

        from histogram import histogram
        I_E = histogram( 'I(E)', [self.Eaxis] )
        
        # for debug
        from pickle import dump
        #dump( distances, open('distance(pixel)-node%d.pkl'%self.mpiRank, 'w') )
        #dump( idpt, open('I(pixel,tof)-node%d.pkl'%self.mpiRank, 'w') )
        dump( mask, open('mask(pixel)-node%d.pkl'%self.mpiRank, 'w') )
        
        from reduction.histCompat.RebinTof2E_batch import istartof2IE
        istartof2IE( idpt, I_E, distances, mask )

        dump( I_E, open('I(Ef)-node%d.pkl' % self.mpiRank,'w') )

        from reduction.histCompat import findPeakPosition
        E = findPeakPosition( I_E, numPoints )
        
        return E * meV


    def _readIdpt(self, run):
        instrument, g = run.getInstrument()
        info.log( 'read data' )
        #we only take the highest level slice.
        #The reason is Pharos Run's getIdpt method
        #cannot take more.
        level0detector = instrument.getDetectorSystem().elements()[0].__class__.__name__.lower() + 'ID'
        if self.detectorSlice:
            sliceInfo = {level0detector: self.detectorSlice[0] }
            idpt = run.getIdpt( **sliceInfo )
        else:
            idpt = run.getIdpt()
        return idpt
    

    pass # end of IncidentEnergySolver_UseElasticPeaks



# version
__id__ = "$Id: MaxIncidentEnergySolver.odb 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
