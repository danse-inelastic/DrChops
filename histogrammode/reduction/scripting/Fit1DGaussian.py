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

class Fit1DGaussian(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Fit 1-dimensional Gaussian function'
    pass


fitg1 = Fit1DGaussian()


from reduction.histCompat.Fit1DFunction import fit1DGaussian
from FunctorFromFunction import FunctorFromFunction as FFF
fitg1.registerEngineFactory(
    'differential evolution',  FFF( fit1DGaussian ) )


fitg1.select( 'differential evolution' )


__all__ = ['fitg1']

# version
__id__ = "$Id$"

# End of file 
