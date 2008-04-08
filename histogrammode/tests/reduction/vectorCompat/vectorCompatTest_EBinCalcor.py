#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "call"
    ]


from reduction.vectorCompat.EBinCalcor import EBinCalcor
from stdVector import vector

datatype = 5  # float


def test_0( **kwds):

    calcor = EBinCalcor( datatype, 25.3, 14000.0)
    
    return True

    
def test_1( **kwds):
    ei = 276.5
    # numbers from Pharos:
    mod2sampDist = 20100.0

    print 'hello'
    
    from math import sqrt
    
    pixDist = sqrt( 4000.0**2 + 0.05**2)

    calcor = EBinCalcor( datatype, ei, mod2sampDist)

    nbins = 10
    
    tofs = [3000.0+i*50 for i in range(nbins)]
    tbb = vector( datatype, tofs)
    ebb = vector( datatype, nbins)

    ebc = EBinCalcor( datatype, ei, mod2sampDist)
    ebc( pixDist, tbb, ebb)

    refBBList = [-1219.97, -743.072, -462.515, -283.634, -162.634, -76.9926,
                 -14.1634, 33.2906, 70.0056, 98.9935]
    
    return utilities.compareFPLists( ebb.asList(), refBBList, 1.0e-2, log)

    
    
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

target = "EBinCalcor"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_EBinCalcor.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

