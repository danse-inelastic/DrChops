#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved

## \package reduction.histCompat.PolynomialFitter
## fit a histogram to a polynomial
##
## this is a wrapper of reduction.vectorCompat.PolynomialFitter


class PolynomialFitter( object):


    def fit( self, histogram, guess = None, weights = None):
        """fit( histogram) -> [best fit params]
        Refine polynomial function's parameters to fit histogram's data at with weights
        given by 1/square of errors, 
        Histogram is assumed to be one-dimensional.
        Inputs:
            histogram: Histogram instance
        Output:
            list of best-fit-parameters
        Exceptions:
        """
        # unpack histogram
        data = histogram.data().storage().asList()
        axis = histogram.axisFromId(1)
        # need bin centers for histogram
        ordinates = axis.binCenters()
        errors = histogram.errors().storage().asList()
        #if weights is None: weights = self.__calcWeights(errors)
        #self._debug.log("ordinates: %s" % ordinates)
        #self._debug.log("data: %s, ordinates: %s, weights:%s" % (
        #    data, ordinates, weights) )
        return self._fitter.fit( ordinates, data )


    def __init__( self, order):
        
        from reduction.vectorCompat.PolynomialFitter import PolynomialFitter
        self._fitter = PolynomialFitter( order )

        import journal    
        self._debug = journal.debug("reduction.histCompat.PolynomialFitter")
        
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
__id__ = "$Id: SimpleFitter.py 953 2006-06-07 19:51:10Z jiao $"

# End of file
