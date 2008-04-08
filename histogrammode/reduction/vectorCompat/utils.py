#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat.utils
## simple functions like Gaussian

from math import sqrt, exp, pi
twoPi = 2*pi
sqrtTwoPi = sqrt(twoPi)

def Gaussian( x, x0, sigma, I=1.0):
    """Gaussian( x, x0, sigma, I) -> gaussian function
    Compute g(x) = 1/( sqrt(2*pi/sigma^2))*exp(- (x-x0)^2/(2*sigma^2))
    Inputs:
        x: point(s) at which to evaluate Gaussian function (float/list)
        x0: center of Gaussian
        sigma: rms std dev of gaussian
        I: prefactor, for convenience (float, default = 1)
    Output:
        value(s)
    Exceptions: None 
    Notes: pass a sequence of x values, get a sequence; pass one x, get one.
    """
    def g(x, x0, sigma, I):
        return I/(sqrtTwoPi*sigma)*exp( -(x-x0)**2/(2*sigma**2))

    try:
        result = g(x, x0, sigma, I) 
    except:
        if "__iter__" in dir( x ):
            result = [g(x1, x0, sigma, I) for x1 in x]
        else:
            raise
        pass
    return result


def simplePeak( x, x0, sigma, I, a=0, b=0, c=0):
    """Simple model for a peak: gaussian plus a quadratic background"""
    def sp( x, x0, sigma, I, a, b, c):
        return a + b*x + c*x**2 + Gaussian(x, x0, sigma, I)
    
    try:
        result = sp(x, x0, sigma, I, a, b, c) 
    except:
        if "__iter__" in dir(x):
            result = [ sp(x1, x0, sigma, I, a, b, c) for x1 in x ]
        else:
            raise
        pass
    return result


# version
__id__ = "$Id: utils.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
