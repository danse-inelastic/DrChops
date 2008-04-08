#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "__call__, simple vals",
    ]


def test_0( **kwds):

    from reduction.vectorCompat.MultScalarErrorProp import MultErrorPropagator

    mep = MultErrorPropagator()
    
    return True

    
def test_1( **kwds):

    from reduction.vectorCompat.MultScalarErrorProp import MultErrorPropagator

    mep = MultErrorPropagator()
    from stdVector import vector
    x = vector( 6, 10, 4.0);
    sigma_x2 = vector( 6, 10, 2.0);

    a = 3
    sigma_a2 = 0.5

    mep.propagate( x, sigma_x2, a, sigma_a2)

    expected = [26.0 for i in range(10)]
    passed = utilities.compareFPLists( expected, sigma_x2.asList(), 1e-20, log)

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

target = "MultScalarErrorProp"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_MultScalarErrorProp.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

