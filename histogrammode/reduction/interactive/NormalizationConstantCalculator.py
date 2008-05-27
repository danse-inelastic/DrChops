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


from FacilityFrontEnd import FacilityFrontEnd

class NCalculator(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Compute normalization constant'
    pass


calcNorm = NCalculator()


from reduction.core.NormalizationConstantFromMonitorData import NormalizationConstantFromMonitorData as Calculator
calcNorm.registerEngineFactory( 'use a monitor', Calculator )


from reduction.core.NormalizationConstantFromIntegratedModeratorCurrent import NormalizationConstantFromIntegratedModeratorCurrent as Calculator

calcNorm.registerEngineFactory( 'use integrated moderator current', Calculator )


calcNorm.select( 'use a monitor' )


__all__ = ['NCalculator', 'calcNorm']

# version
__id__ = "$Id$"

# End of file 
