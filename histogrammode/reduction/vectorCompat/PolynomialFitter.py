#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved

## \package reduction.vectorCompat.PolynomialFitter
## fit data to a polynomial

from fit_polynomial_QRFactorization import *
#fitter function ordered in the order of the polynomial
fitters = [
    None,
    linfit,
    qfit,
    ]
   
 
class PolynomialFitter( object):
    """fitter to fit a data to a polynomial"""

    def fit( self, x, y ):
        x = tonumarray(x); y = tonumarray(y)
        
        order = self._order
        try: fitter = fitters[ order ]
        except:
            raise ValueError, \
                  "don't know to to fit to %s-order polynomial" % order
        
        self._result = fitter( x, y )
        return self._result


    def result( self):
        """result() -> most recent result (could be None)"""
        return self._result
    

    def __init__( self, order):
        """@param order: order of polynomial
        """
        self._order = order
        self._result = None
        return


def tonumarray( anything ):
    from stdVector.StdVector import StdVector
    import numpy
    if isinstance(anything, StdVector): return anything.asNumarray().copy()
    if isinstance(anything, list) or isinstance(anything, tuple) :
        return numpy.array(anything)
    if isinstance(anything, numpy.ndarray): return anything
    raise ValueError , "don't know how to convert %s to a number list" % (
        anything,)
    

# version
__id__ = "$Id: PolynomialFitter.py 405 2005-05-11 03:16:42Z tim $"

# End of file
