#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "fit a Gaussian to something",
    "fit a simple peak profile to something",
    "fit a simple peak profile to something, using some defaults",
    ]
 

from reduction.vectorCompat.SimpleFitter import SimpleFitter
from reduction.vectorCompat.utils import Gaussian, simplePeak


def test_0( **kwds):

    fitter = SimpleFitter( Gaussian)
    
    return True


def test_1( **kwds):

    from math import sqrt

    fitter = SimpleFitter( Gaussian)

    # ordinates
    x = [1.0*i for i in range(-5,6)]
    
    # slightly perturbed Gaussian with x0 = 0.5, sigma=1.5, I=1.33
    gdata = [0.00044713, 0.00373309, 0.0244125, 0.0837929, 0.225274, 0.31788, 0.351343, 0.2038200, 0.0926132, 0.0220875, 0.0041260508]

    weights = [1/sqrt( gdatum) for gdatum in gdata]

    log("weights: %s" % weights)

    result = fitter.fit( gdata, x, weights, [0.3, 1.6, 1.4])

    log("result was %s" % result)
    return True

    
def test_2( **kwds):

    from math import sqrt

    fitter = SimpleFitter( simplePeak)

    # ordinates
    xs = [1.0*i for i in range(-5,6)]
    
    # slightly perturbed Gaussian with x0 = 0.5, sigma=1.5, I=1.33
    gdata = [0.00044713, 0.00373309, 0.0244125, 0.0837929, 0.225274, 0.31788, 0.351343, 0.2038200, 0.0926132, 0.0220875, 0.0041260508]

    a = 5.2; b = 0.3; c = -0.015

    for i,x in enumerate( xs):
        gdata[i] += a + b*x + c*x**2

    weights = [1/sqrt( gdatum) for gdatum in gdata]

    result = fitter.fit( gdata, xs, weights, [0.3, 1.6, 1.4, 2.0, 0.9, 0.1])

    log("result was %s" % result)
    return True

    
def test_3( **kwds):

    from math import sqrt

    fitter = SimpleFitter( simplePeak)

    # ordinates
    xs = [1.0*i for i in range(-5,6)]
    
    # slightly perturbed Gaussian with x0 = 0.5, sigma=1.5, I=1.33
    gdata = [0.00044713, 0.00373309, 0.0244125, 0.0837929, 0.225274, 0.31788, 0.351343, 0.2038200, 0.0926132, 0.0220875, 0.0041260508]

    a = 5.2

    for i,x in enumerate( xs):
        gdata[i] += a

    weights = [1/sqrt( gdatum) for gdatum in gdata]

    result = fitter.fit( gdata, xs, weights, [0.3, 1.6, 1.4, 2.0])

    log("result was %s" % result)
    return True

    
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


import  utilities

target = "SimpleFitter"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_SimpleFitter.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

