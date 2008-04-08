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


## \package reduction.core.VDataProcessor
## Processing
## routines regarding vanadium calibration data
##
## Vanadium data is usually used to compute detector efficiency
## and detector mask.
## This class provides some methods to do those things.
##


import journal, math

jrnltag = "reduction.core.VDataProcessor"
debug = journal.debug( jrnltag )
warning = journal.warning( jrnltag )


from histogram import histogram


from ParallelComponent import ParallelComponent


class VDataProcessor( ParallelComponent ):

    "processing routines regarding vanadium calibration data"


    def __init__(self, vrun,
                 ei = None, whitebeam = True,
                 tof2E = None):
        """In this Vanadium data processor, we are only concerned
        with the I(det,tof) histogram gathered for vanadium run.

        ei: incident energy. leave it as None if whitebeam is true
        whitebeam: is the calibration done with whitebeam?
        tof2E: rebinner to rebin I(*,tof) to I(*,E)
        """

        if not whitebeam and ei is None:
            raise NotImplementedError , \
                "This processor can only deal with white-beam data, "\
                "or a monochromatic beam (for which the incident "\
                "energy should be specified. )"\
                "ei = %s, whitebeam = %s" % (
                ei, whitebeam )
        self.Idettof = vrun.getIdt()
        self.detaxes = self.Idettof.axes()[:-1]
        self.vrun = vrun
        self.ei = ei
        self.whitebeam = whitebeam

        #distance of all detectors
        from getDetectorInfo import getDistances
        instrument, geometer = vrun.getInstrument()
        self.distance_det = getDistances(instrument, geometer, self.detaxes )
        self.mod2sample = geometer.distanceToSample( instrument.getModerator() )
        
        if tof2E is None:
            from Tof2E import Tof2E 
            tof2E = Tof2E()
            pass
        self.tof2E = tof2E

        self._Idetstore = {}
        self._axisStore = {}
        return


    def calibrationConstants(self, energy = None):
        '''obtain calibration constants as a function of detectorID

        inputs:
          energy(optional): The neutron energy at which the calibration
              process is done.
        return: calibration constants (histogram)
        '''
        return self.runMasterNodeOnly( 88, self.calibrationConstants1, energy )


    def getMask(self, energy = None):
        return self.runMasterNodeOnly( 66, self.getMask1, energy )


    def calibrationConstants1(self, energy = None):
        energy = self._checkEnergy( energy )
        
        #I(..., det) for given energy. ... are packID, etc etc 
        Idet = self.getIdet( energy )

        instrument, geometer = self.vrun.getInstrument()
        #scatterin angle vs det
        from getDetectorInfo import getScatteringAngles
        sa_det = getScatteringAngles(instrument, geometer, self.detaxes)
        
        #theoretical efficiency
        te_det = self.theoreticalEfficiency( energy )
        te_det = self._checkTheoreticalEfficiency( te_det )

        #calculator for transmission thru vanadium sample
        from VanadiumTransmissionCalculator import calculator
        calculator.setSampleAssembly( self.vrun.getSampleAssembly() )
        
        from histogram import histogram, pqvalue
        tc_det = histogram(
            'transmission coefficients',
            self.detaxes,
            fromfunction = lambda *detIDs: calculator( sa_det[ detIDs ][0], energy )
            )

        ret = Idet/tc_det/te_det

        #save data for debug
        dump( te_det, 'vanadium-TheoreticalEfficiency(detIDs).pkl')
        dump( tc_det, 'vanadium-TransmissionCoefficients(detIDs).pkl')
        dump( Idet, 'vanadium-I(detIDs).pkl')
        dump( ret, 'vanadium-correctedI(detIDs).pkl')

        #create arrays
        def arr( h ):
            ret = h.data().storage().asNumarray().copy()
            ret.shape = -1,
            return ret
        transmission_coeffs = arr(tc_det)
        uncorrected = arr(Idet)
        phis = arr(sa_det)
        theoretical_efficiencies = arr(te_det)
        corrected = arr(ret)
        
        #sort phi so that plotting is easier
        o = phis.argsort()
        save = [
            ('phi', phis[o]),
            [('uncorrected', uncorrected[o]),
             ('transmission_coeffs', transmission_coeffs[o]),
             ('theoretical_efficiencies', theoretical_efficiencies[o]),
             ('corrected', corrected[o]),
             ],
            ]
        dump( save, 'vanadiumcalibration-results.pkl' )
        return ret
    

    def theoreticalEfficiency(self, energy):
        from getDetectorInfo import getTheoreticalEfficiencis
        instrument, geometer = self.vrun.getInstrument()
        return getTheoreticalEfficiencis(energy, instrument, self.detaxes )
        

    def getMask1(self, energy):
        """calculate a detector mask

        The mask depends on the neutron energy of interests
        """
        energy = self._checkEnergy(energy)
        Idet = self.getIdet( energy )
        from MaskFromVanadiumData import findBadDetectors
        debug.log('start find bad detectors')
        badDetectors = findBadDetectors( Idet )
        debug.log('done')
        from instrument import mask
        return mask( excludedDetectors = badDetectors )


    def getIdet(self, energy):
        """calculate I(det) histogram for the given energy

        I(det) histogram at given energy is the basis of almost
        all computations in Vanadium calibration.

        The algorithm is simply to first get the
        I(det,tof) histogram, and then convert the histogram
        to I(det,E), and then get a slice of it for which
        the energy is set to the user-specified value
        """
        debug.log( 'enter getIdet' )
        import reduction.units as units

        # the data we need to work on
        Idt = self.Idettof

        # tof axis
        taxis = Idt.axisFromName( 'tof' )
        tunit = taxis.unit()
        second2tunit = units.time.second / tunit

        #neutron velocity
        from reduction.utils.conversion import e2v
        velocity = e2v( energy/units.energy.meV )

        #distance from detector to sample
        distance_det = self.distance_det
        mod2sample = self.mod2sample
        #the function that returns the intensity of the given detector
        #at the tof bin corresponding to the given energy
        def _(*detIDs):
            detIDs = tuple(detIDs)
            dist = ( distance_det[ detIDs ][0] + mod2sample )/units.length.meter
            tof = dist/velocity * second2tunit
            args = detIDs + (tof,)
            return Idt[ args ][0]

        #result to be returned
        ret = histogram(
            "I(det)",
            self.detaxes,
            fromfunction = _)

        #if the counts is too low, the statistics won't allow to do calibration
        #accurately. So we better check for that
        arr = ret.data().storage()
        average_counts = arr.sum()/arr.size()
        if average_counts < 10000:
            msg = "average counts is smaller than 10000. Statistics is not "\
                  "good enough. \n"\
                  "We will simply use energy-independent total intensity\n"
            warning.log( msg )
            ret = Idt.sum('tof')
            pass
                         
        return ret


    def _checkEnergy(self, energy):
        "check sanity of energy input"
        if not self.whitebeam and energy is not None: 
            #if not whitebeam, then we have monochromatic 
            #beam. The given energy must be the same as
            #the incident energy of the vanadium run
            assert abs( (energy/self.ei)-1 )< 1.e-3 , \
                   "Monochromatic beam calibraiton data can only provide "\
                   "calibraiton constants for one particular energy. " \
                   "Calibration data neutron energy = %s, request energy = %s" \
                   % (self.ei, energy)
            energy = self.ei
            pass
        if energy is None: energy = self.ei
        return energy


    def _checkTheoreticalEfficiency(self, te_det):
        'check sanity of theoretical efficiency'
 	tes = te_det.data().storage()
        avetes = tes.sum()/tes.size()
        #make sure no data is zero
        te_det += avetes/1.e10, 0.
        return te_det
    
    pass # end of VDataProcessor
    

from pyre.units.length import meter, mm
from pyre.units.energy import meV
from pyre.units.time import microsecond
from pyre.units.angle import degree

from getDetectorInfo import getDistances, getPressures

from reduction.utils.hpickle import dump

# version
__id__ = "$Id$"

# End of file
