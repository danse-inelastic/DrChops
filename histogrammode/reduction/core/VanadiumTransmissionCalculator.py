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


## \package reduction.core.VanadiumTransmissionCalculator
## Calculates transmission probablity of neutrons
## going through a given vanadium calibration sample.
##
## This calculator is useful in calibration.
## To obtain calibration constants of detectors, we need to
## calculate several theoretical predictions of variations
## of detector intensities.
## The absorption of the vanadium sample itself is one
## reason of the intensity variation among detectors.
## The most usual phenomena resulted from this absorption
## is the "dark angle".
## This calculator calculates the tranmission of neutrons
## through the sample, and return the transmission as
## a function of the scattering angle.
##


class VanadiumTransmissionCalculator:

    '''Calculator that
    calculates transmission probablity of neutrons
    going through a given vanadium calibration sample.
    '''

    def setSampleAssembly(self, sampleassembly):
        """set the sample assembly that this calculator will work on"""
        assert sampleassembly.name.lower().find( "vanadium") != -1, \
               '''This is not a vanadium sample: %s''' % sampleassembly.name
        self.calculator = _vTxCalcorFactory( sampleassembly )
        return


    def __call__(self, scattering_angle, energy ):
        """__call__( scattering_angle, energy ) --> transmission coeff

        all physical quantities must have units attached.
        
        scattering_angle: scattering 
        energy: neutron energy

        return: transmission coefficient. 
        """
        return self.calculator( scattering_angle, energy )
    

    pass # end of VanadiumTransmissionCalculator


calculator = VanadiumTransmissionCalculator()


#dispatcher implementation
class _VTxCalcorFactory:


    def __call__(self, sampleassembly):
        self.sampleassembly = sampleassembly
        type = sampleassembly.__class__.__name__
        method = getattr(self, 'on'+type)
        return method( sampleassembly )
    

    def onVanadiumPlate(self, vanadiumPlate):
        width, height, thickness = vanadiumPlate.dimensions()
        darkAngle = vanadiumPlate.darkAngle

        from reduction.histCompat.VSampleParams import VSampleParams
        vsp = VSampleParams( darkAngle, thickness, width )
        from reduction.histCompat.VanPlateTx import VanPlateTx
        return VanPlateTx( vsp )
    
    pass # end of _VTxCalcorFactory

_vTxCalcorFactory = _VTxCalcorFactory()


# version
__id__ = "$Id$"

# End of file

