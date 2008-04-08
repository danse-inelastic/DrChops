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


## \package reduction.core.DifferentialEvolution1DFunctionFitter
## 1D function fitter implemented using differential evolution
## optimization algorithm.
##
## The DE algorithm is actually from Patrick Hung's mystic package.
##


from Abstract1DFunctionFitter import Abstract1DFunctionFitter as base

class DifferentialEvolution1DFunctionFitter( base ):

    ''' 1D function fitter use DE algorithm
    '''

    def __call__(self, histogram, functor, boxConstraints ):
        '''__call__( histogram, functor, boxConstraints ): fit histogram to functor
        
    histogram: y(x) data curve
    functor: the function to fit, for example
    
        def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

    boxConstraints: constraints of parameters defined as a box
    '''
        from reduction.histCompat.Fit1DFunction import Fit1DFunction
        fit = Fit1DFunction( functor, minimizer = self.minimizer,
                                plotter = self.plotter )
        return fit( histogram, boxConstraints )


    def __init__(self, minimizer = None, plotter = None):
        '''__init__(minimizer, plotter)

        minimizer: the engine to minimize the penalty function
        plotter: plotting facility
        '''
        self.minimizer = minimizer
        self.plotter = plotter
        return        
        

    pass # end of DifferentialEvolution1DFunctionFitter



# version
__id__ = "$Id$"

# End of file 
