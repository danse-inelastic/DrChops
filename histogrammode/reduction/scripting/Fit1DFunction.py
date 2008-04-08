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

class Fit1DFunction(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Fit 1-dimensional function'
    pass


fit1 = Fit1DFunction()


from reduction.core.DifferentialEvolution1DFunctionFitter import DifferentialEvolution1DFunctionFitter as Fitter
fit1.registerEngineFactory( 'differential evolution', Fitter )


fit1.select( 'differential evolution' )


__all__ = ['fit1']

# version
__id__ = "$Id$"

# End of file 
