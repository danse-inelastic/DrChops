#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat.SimpleFitter
## fit x-y data to a 1-D function


class SimpleFitter( object):
    """Simple interface to complex problem."""

    def fit( self, data, xvals, weights, guess):

        def resids( p, y, x, weights, functor):
            args = [x]
            for num in p:
                args.append(num)

            vals = apply( functor, args)
            resid = [ww*(yy-val) for (ww, yy, val) in zip( weights, y, vals)]
            return resid
        
        from scipy.optimize import leastsq

        self._result = leastsq( resids, guess,
                                args=(data, xvals, weights, self._functor))

        return self._result[0]


    def result( self):
        """result() -> most recent result (could be None)"""
        return self._result
    

    def __init__( self, functor):
        self._functor = functor
        self._result = None
        return


# version
__id__ = "$Id: SimpleFitter.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
