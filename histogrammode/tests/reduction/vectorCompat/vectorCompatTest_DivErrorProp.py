#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "propagate, simple vals",
    ]


def test_0( **kwds):

    from reduction.vectorCompat.DivErrorProp import DivErrorPropagator

    mep = DivErrorPropagator()
    
    return True

    
def test_1( **kwds):

    from reduction.vectorCompat.DivErrorProp import DivErrorPropagator

    mep = DivErrorPropagator()
    from stdVector import vector
    x = vector( 6, 10, 2.0);
    sigma_x2 = vector( 6, 10, 3.0);

    y = vector( 6, 10, 5.0)
    sigma_y2 = vector( 6, 10, 7.0)

    output = vector( 6, 10, 0.0)

    output = mep.propagate( x, sigma_x2, y, sigma_y2, output)

    expected = [0.1648 for i in range(10)]
    passed = utilities.compareFPLists( expected, output.asList(), 1e-16, log)

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

target = "DivErrorProp"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_DivErrorProp.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

