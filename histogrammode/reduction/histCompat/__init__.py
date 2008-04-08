#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.histCompat
## Histogram-level classes for reduction package
##
## "python histogram compatible" layer histCompat allows developers to deal with objects with
## more physics meanings. A
## <a href="../../../histogram/histogram/html"> histogram </a>
## is an object consisting of axes and datasets and meta data. In the histCompat layer,
## histograms are our focus. Classes in this layer only take histograms as arguments,
## and implementations of thos classes decompose histograms to vectos and call the
## corresponding methds in the vectorCompat layer.
##


def findPeakPosition( histogram, n = 8 ):
    """find the position of the highest peak in a histogram

    The algorithm is
     1. find the highest point
     2. take 2n+1 points around the highest point
     3. fit the curve (2n+1 points around the highest point)
        to a parabolic, and return the position of the center
    """
    ys = histogram.data().storage().asNumarray()
    from numpy import argmax
    maxyindex = argmax(ys)
    startindex = max( maxyindex - n, 0 )
    stopindex = maxyindex + n
    xaxis = histogram.axisFromId( 1 )
    x1 = xaxis[ startindex ]/xaxis.unit() 
    x2 = xaxis[ stopindex ]/xaxis.unit()
    subhist = histogram[ (x1,x2) ]
    from PolynomialFitter import PolynomialFitter
    fitter = PolynomialFitter( 2 )
    a = fitter.fit( subhist )
    return -a[1]/2./a[2]


# version
__id__ = "$Id: __init__.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
