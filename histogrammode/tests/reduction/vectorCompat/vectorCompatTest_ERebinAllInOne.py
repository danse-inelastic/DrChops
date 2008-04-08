#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate",
    "call"
    ]


from reduction.vectorCompat.ERebinAllInOne import Rebinner
from ndarray.StdVectorNdArray import NdArray

datatype = 6   # double
nTBins = 9
nEBins = 9
e_i = 276.5
mod2Samp = 20100.0

dt = 50.0
de = 10.0

def test_0( **kwds):

    rebinner = Rebinner( datatype, nTBins, nEBins, e_i, mod2Samp,
                         dt, de, False, 0.05)

    return True

    
def test_1( **kwds):

    tofs = [3000.0 + i*dt for i in range(nTBins+1)]
    tbb = NdArray( datatype, tofs)
    nrgs = [-50.0 + i*de for i in range(nEBins+1)]
    ebbn = NdArray( datatype, nrgs)

    import math
    distance = math.sqrt( 4000.0**2+0.05**2)

    rebinner = Rebinner( datatype, nTBins, nEBins, e_i, mod2Samp, dt, de,
                         False, 0.05)

    indata = NdArray( datatype, nTBins, 1.0)
    inerrs = NdArray( datatype, nTBins, 2.0)
    outdata = NdArray( datatype, nEBins, 0.0)
    outerrs = NdArray( datatype, nEBins, 0.0)

    rebinner( distance, tbb, ebbn, indata, outdata, inerrs, outerrs)

##     refList = [0.7958087239, 0.7958087239, 0.7958087239, 
##                0.9031594330, 1.0536518999, 1.0536518999, 
##                1.0536518999, 1.0536518999, 1.2604285222]
##     r2l =[1.5916174478, 1.5916174478, 1.5916174478, 1.8063188660, 2.1073037998, 2.1073037998, 2.1073037998, 2.1073037998, 2.5208570444]

    from ERebinAllInOne import ERebinAllInOne
    refList = ERebinAllInOne(e_i, mod2Samp/1000., tofs, distance/1000., nrgs,
                             [1.0 for i in range( nTBins )] )
    r2l = ERebinAllInOne(e_i, mod2Samp/1000., tofs, distance/1000., nrgs,
                         [2.0 for i in range( nTBins )] )

    passedData = utilities.compareFPLists( refList, outdata.asList(), 1.0e-5,
                                           log)
    passedErrors = utilities.compareFPLists( r2l, outerrs.asList(),
                                             1.0e-5, log)

    return passedData and passedErrors

    
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

target = "ERebinAllInOne"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_ERebinAllInOne.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file

