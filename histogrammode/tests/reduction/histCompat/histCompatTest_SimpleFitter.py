#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "fit a Gaussian to something",
    "fit a simple peak profile to something",
##     "fit a simple peak profile to something, using some defaults",
    ]

from reduction.histCompat.SimpleFitter import SimpleFitter
from reduction.vectorCompat.utils import Gaussian, simplePeak


from ndarray.StdVectorNdArray import NdArray


def test_0( **kwds):

    fitter = SimpleFitter( Gaussian)

    return True

    
def test_1( **kwds):

    from math import sqrt

    dtype = 6 #double
    
    fitter = SimpleFitter( Gaussian)

    # ordinates
    x = NdArray( dtype, [1.0*i-0.5 for i in range(-5,7)])
    
    # slightly perturbed Gaussian with x0 = 0.5, sigma=1.5, I=1.33
    gdataList = [0.00044713, 0.00373309, 0.0244125, 0.0837929, 0.225274,
                 0.31788, 0.351343, 0.2038200, 0.0926132, 0.0220875,
                 0.0041260508]
    gdata = NdArray( dtype, gdataList)
    errors = NdArray( 6, [sqrt( gdatum) for gdatum in gdataList])

##     log("errors: %s" % errors.asList())
    
    from histogram import Histogram, NdArrayDataset, Axis
    ax = Axis.Axis( storage=x)
    ds = NdArrayDataset.Dataset( storage=gdata)
    errorDS = NdArrayDataset.Dataset( storage=errors)

    hist = Histogram.Histogram( data = ds, errors=errorDS, axes=[ax])

    result = fitter.fit( hist, [0.3, 1.6, 1.4])
    expected = [ 0.5, 1.5, 1.33]
    passed = utilities.compareFPLists( result, expected, 5.0e-3, log)
    log("result was %r, should be close to %s" % (result, expected) )
    return passed


def test_2( **kwds):

    from math import sqrt
    from histogram import Histogram, NdArrayDataset, Axis

    dtype = 6 #double

    # ordinates
    xlist = [1.0*i-0.5 for i in range(-5,7)]
    xs = NdArray( dtype, xlist)
    ax = Axis.Axis( storage=xs)
    
    # slightly perturbed Gaussian with x0 = 0.5, sigma=1.5, I=1.33
    gdataList = [0.00044713, 0.00373309, 0.0244125, 0.0837929, 0.225274,
                 0.31788, 0.351343, 0.2038200, 0.0926132, 0.0220875,
                 0.0041260508]
    a = 5.2; b = 0.3; c = -0.015
    for i,x in enumerate( ax.binCenters()):
        gdataList[i] += a + b*x + c*x**2
    gdata = NdArray( dtype, gdataList)
    errors = NdArray( 6, [sqrt( gdatum) for gdatum in gdataList])

    ds = NdArrayDataset.Dataset( storage=gdata)
    errorDS = NdArrayDataset.Dataset( storage=errors)
    hist = Histogram.Histogram( data = ds, errors=errorDS, axes=[ax])

    fitter = SimpleFitter( simplePeak)
    result = fitter.fit( hist, [0.3, 1.6, 1.4, 2.0, 0.9, 0.1])
    expected = [0.50, 1.5,
                1.33, 5.2,
                0.3, -0.015]
    passed = utilities.compareFPLists( result, expected, 1.e-2, log)
    return passed

    
# ------------- do not modify below this line ---------------


def run( **kwds):
    
    allPassed = True
    
    for i, aspect in enumerate( aspects):
        run = eval( 'test_' + str(i))
        utilities.preReport( log, target, aspect)
        passed = run( **kwds)
        utilities.postReport( log, target, aspect, passed)
        allPassed = allPassed and passed

    return allPassed


target = "SimpleFitter"
import journal
log = journal.info( target).log
import utilities

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()

    journal.debug("reduction.histCompat").activate()
    
    run()

# version
__id__ = "$Id: histCompatTest_SimpleFitter.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

