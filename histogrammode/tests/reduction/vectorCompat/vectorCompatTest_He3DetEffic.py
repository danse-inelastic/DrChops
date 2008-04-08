#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "call single",
    "call vector",
    "graph test",
    ]

from reduction.vectorCompat.He3DetEffic import He3DetEffic
from math import sqrt
from ndarray.StdVectorNdArray import NdArray

dtype = 6


def test_0( **kwds):

    de = He3DetEffic( 10.0, 12.7, 450, 5)

    return True

    
def test_1( **kwds):

    de = He3DetEffic( 10.0, 12.7, 450, 5)
    effic = de( 25.3)

    log("Returned %s" % effic)
    return True

    
def test_2( **kwds):

    de = He3DetEffic( 10.0, 12.7, 450, dtype)
    energies = NdArray( dtype, [25.3+1.0*i for i in range(5,-6,-1)])
    effic = de( energies)

    log("Returned %s" % effic.asList())
    return True


def test_3( **kwds):
    if 'noGraph' in kwds:
        if kwds['noGraph'] == True:
            log("skipping graph test")
            return True
    try:
        import Gnuplot

        g = Gnuplot.Gnuplot()

        de = He3DetEffic( 10.0, 12.7, 450, dtype)
        energies = NdArray( dtype, [1000-1.0*i for i in range(1000)])
        effic = de( energies)

        g('set xlabel "energy (meV)"')
        g('set ylabel "fraction absorbed"')
        g.plot( Gnuplot.Data( energies.asList(), effic.asList(), with='lines'))
        raw_input("Press enter to continue")
        return True
    except ImportError:
        log("plotting unavailable--this test did not fail, but...")
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

target = "He3DetEffic"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_He3DetEffic.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file

