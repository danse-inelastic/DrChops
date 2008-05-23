#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from FacilityFrontEnd import *

class GetCalibrationConstants(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Compute calibration constants'
    pass


getCC = GetCalibrationConstants()


class CCfromWhiteBeamV:

    def __init__(self):
        '__init__()'
        return

    def __call__(self, vRun, energy):
        '__call__(vRun, energy): get calibration constants for the given energy'
        from reduction.core.VDataProcessor import VDataProcessor
        p = VDataProcessor( vRun, whitebeam = True )
        return p.calibrationConstants(energy)
    
    pass # CCfromWhiteBeamV
getCC.registerEngineFactory('white beam V',  CCfromWhiteBeamV)


getCC.select( 'white beam V' )


__all__ = ['GetCalibrationConstants', 'getCC']



# version
__id__ = "$Id$"

# End of file 
