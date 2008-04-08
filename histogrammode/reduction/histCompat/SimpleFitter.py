#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.histCompat.SimpleFitter
## fit a histogram to a function
##
## The implementation uses scipy.optimize.
##
## this is a wrapper of reduction.vectorCompat.SimpleFitter



class SimpleFitter( object):

    def fit( self, histogram, initParamValues):
        """fit( histogram, initParamVals) -> [best fit params]
        Refine function's parameters to fit histogram's data at with weights
        given by 1/square of errors, starting at intial parameter values.
        Histogram is assumed to be one-dimensional.
        Inputs:
            histogram: Histogram instance
            initParamVals: list of initial parameters 
        Output:
            list of best-fit-parameters
        Exceptions:
        Notes: (1) initial values for fit parameters are passed as a whole to
               the fitting routine, so it is user's responsibility to provide
               a list of parameters that matches the syntax of the fit
               function. """
        # unpack histogram
        data = histogram.data().storage().asList()
        axis = histogram.axisFromId(1)
        # need bin centers for histogram
        ordinates = axis.binCenters()
        errors = histogram.errors().storage().asList()
        weights = self.__calcWeights(errors)
##         self._debug.log("ordinates: %s" % ordinates)
        self._debug.log("data: %s, ordinates: %s, weights:%s, initParams: %s" % (
            data, ordinates, weights, initParamValues) )
        return self._fitter.fit( data, ordinates, weights, initParamValues)


    def __init__( self, functor):
        
        from reduction.vectorCompat.SimpleFitter import SimpleFitter
        self._fitter = SimpleFitter( functor)

        import journal    
        self._debug = journal.debug("reduction.histCompat.SimpleFitter")
        
        return


    def __calcWeights(self, errors):
        """calculate weights from given error bars
        it is assumed that all errors are no less than zero
        """
        #return [1.0 for e in errors]
        for error in errors: assert error >=0.0, "error must not be negative: %s" % error
        
        #find the minimum err that is positive
        min_err = max(errors)
        for err in errors:
            if err>0. and err < min_err: min_err = err
            continue
        
        #so we can calculate the max weight we want to use
        from math import sqrt
        max_wt = 1.0/sqrt(min_err)

        #weights 
        weights = []
        for err in errors: 
            if err == 0.0 : weight = max_wt
            else: weight = 1.0/sqrt(err)
            weights.append(weight)
        return weights


# version
__id__ = "$Id: SimpleFitter.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
