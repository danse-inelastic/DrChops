#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "simple test"
    ]

from reduction.vectorCompat.AddScalarErrorProp import AdditionErrorPropagator

def test_0( **kwds):

    prop = AdditionErrorPropagator()

    return True


def test_1( **kwds):

    prop = AdditionErrorPropagator()

    from stdVector import vector
    v1 = vector( 6, 10, 4.0)
    v2 = vector( 6, 10, 0.0)

    prop.propagate( v1, 9.0, v2)

    passed = utilities.compareFPLists( v2.asList(), [13.0 for i in range(10)],
                                       1.e-20, log)

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

target = "AddScalarErrorProp"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_AddScalarErrorProp.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

