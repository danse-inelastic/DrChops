#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "basic check"
    ]


def test_0( **kwds):

    from reduction.vectorCompat.DivScalarErrorProp import DivErrorPropagator

    dep = DivErrorPropagator()
    log("instantiated")

    from stdVector import vector
    data = vector( 6, 5, 2.0)
    errors = vector( 6, 5, 3.0)
    a = 5.0
    sigma_a2 = 7.0

    dep.propagate( data, errors, a, sigma_a2)

    expected = [1/(a**4)*sigma_a2*4.0 + 1/(a**2)*3.0 for i in range(5)]

    passed = utilities.compareFPLists( errors.asList(), expected, 1e-20, log)

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


import  utilities

target = "DivErrorPropagator"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_DivScalarErrorProp.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

