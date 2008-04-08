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


## \package reduction.core.Abstract1DFunctionFitter
## Abstract base class for 1D function fitters.
##
## Any subclass should be able to fit a histogram to a function and
## return the best fitting parameters.
##
## Names of subclasses should contain the string "1DFunctionFitter"
##


class Abstract1DFunctionFitter:

    '''abstract base calss for 1D function fitter

    histogram: y(x) data curve
    functor: the function to fit, for example
    
        def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

    boxConstraints: constraints of parameters defined as a box
    '''

    def __call__(self, histogram, functor, boxConstraints ):
        raise NotImplementedError

    pass # end of Abstract1DFunctionFitter


# version
__id__ = "$Id$"

# End of file 
