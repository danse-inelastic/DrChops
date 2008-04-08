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

class EiSolver(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Compute incident energy'
    pass


solveEi = EiSolver()


from reduction.core.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as Solver
solveEi.registerEngineFactory( 'use monitors', Solver )


from reduction.core.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks as Solver

solveEi.registerEngineFactory( 'use elastic peaks', Solver )


solveEi.select( 'use elastic peaks' )


__all__ = ['EiSolver', 'solveEi']

# version
__id__ = "$Id$"

# End of file 
