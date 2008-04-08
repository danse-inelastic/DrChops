#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 T. M. Kelley
#                   (C) Copyright 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.vectorCompat.SimplePeak
## a gaussian peak


from reduction.vectorCompat.utils import simplePeak

class SimplePeak:
    """wraps reduction.vectorCompat.utils.simplePeak()"""

    def __call__( self, x, x0, sigma, I, a=0, b=0, c=0):
        """simplePeak( x, x0, sigma, I, a=0, b=0, c=0) -> gaussian+a+bx+cx^2
        Simple model for a peak: gaussian plus a quadratic background
        Inputs:
            x: ordinate(s) (Python sequence or float)
            x0: center of Gaussian
            sigma: Gaussian r.m.s. std. dev.
            I: Gaussian integrated intensity
            a, b, c: quadratic coefficients, defaults 0
        Output:
            simple peak point(s)
        Exceptions: None known
        Notes: If you pass a list/tuple for x, this returns a list, otherwise,
        returns a single float"""
        return simplePeak( x, x0, sigma, I, a, b, c)


    def __init__(self): return
    


# version
__id__ = "$Id: SimplePeak.py 1401 2007-08-29 15:36:44Z linjiao $"

# Generated automatically by PythonMill on Wed May 11 07:32:05 2005

# End of file 
