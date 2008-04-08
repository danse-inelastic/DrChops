#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "call"
    ]


from reduction.histCompat.EBinCalcor import EBinCalcor


from ndarray.StdVectorNdArray import NdArray


datatype = 6  # double
e_i = 276.5
mod2sampDist = 20100.0


def test_0( **kwds):

    calcor = EBinCalcor( datatype, e_i, mod2sampDist)

    return True


def test_1( **kwds):

    import math
    pixelDist = math.sqrt( 4000.0**2 + 0.05**2)
    
    nbins = 10
    
    # construct histograms with appropriate axes
    from histogram.Histogram import Histogram
    from histogram.Axis import Axis
    from histogram.NdArrayDataset import Dataset
    
    tofs = [3000.0+i*50 for i in range(nbins)]
    tbb = NdArray( datatype, tofs)
    ebb = NdArray( datatype, nbins)

    dummyStore = NdArray( datatype, nbins-1)
    
    tofAxis = Axis( "tof", "meV", storage = tbb)
    tofDataset = Dataset( "tdata", "1", shape = [nbins-1],
                          storage = dummyStore)
    tofHistogram = Histogram( "tofHist", data=tofDataset, errors = tofDataset,
                              axes = [tofAxis])
    
    energyAxis = Axis( "energy", "meV", storage = ebb)
    energyDataset = Dataset( "edata", "1", shape = [nbins-1],
                             storage = dummyStore)
    energyHistogram = Histogram( "energyHist", data=energyDataset,
                                 errors = energyDataset, axes = [energyAxis])
    
    # call
    calcor = EBinCalcor( datatype, e_i, mod2sampDist)
    calcor( pixelDist, tofHistogram, energyHistogram)

    # check axes to make sure that
    # 1. time axis unchanged ...
    log("Checking tof axis")
    passedTOF = utilities.compareFPLists( tofs, tofAxis.binBoundariesAsList(),
                                          1.0e-20, log)

    # 2. ... and energy axis is correctly changed
    log("Checking energy axis")
    expected = [-1219.96701621300098850043, -743.07195244362480934797,
                -462.51492179714080066333, -283.63394325099528714418,
                -162.63431067499539040000, -76.99257889707347146668,
                -14.16341090766355037545, 33.29059169485528713039,
                70.00559848310093968848, 98.99346153933967684679]
    passedEnergy = utilities.compareFPLists( expected,
                                             energyAxis.binBoundariesAsList(),
                                             1.0e-10, log)
    
    passed = passedTOF and passedEnergy
    return passed

    
# ------------- do not modify below this line ---------------


def run( **kwds):
    
    allPassed = True
    
    for i, aspect in enumerate( aspects):
        run = eval( 'test_' + str(i))
        #utilities.preReport( log, target, aspect)
        passed = run( **kwds)
        #utilities.postReport( log, target, aspect, passed)
        allPassed = allPassed and passed

    return allPassed


import journal

target = "EBinCalcor"

log = journal.info( target).log
import utilities

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()

##     journal.debug("histogram").activate()
    
    run()

# version
__id__ = "$Id: histCompatTest_EBinCalcor.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file

