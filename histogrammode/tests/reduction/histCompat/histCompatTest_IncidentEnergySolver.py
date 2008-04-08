#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate/initialize",
    "fit to bogus numbers"
    ]

from reduction.histCompat.IncidentEnergySolver import IncidentEnergySolver


def test_0( **kwds):
    solver = IncidentEnergySolver()
    return True


def test_1( **kwds):

    import journal
    journal.debug("reduction.histCompat").activate()
    
    from ndarray.StdVectorNdArray import NdArray
    dtype = 6 
##     tofList = [1.0*i for i in range(101)]
##     tof = NdArray( dtype, tofList)
##     from histogram.Axis import Axis
##     tofds = Axis( storage=tof)
    from histogram import createContinuousAxis, arange
    tofds = createContinuousAxis( "tof", "microsecond", arange( 0.5, 100.5, 0.5) )
    
    # construct "monitor 2"
    from reduction.vectorCompat.utils import simplePeak
    d2List = simplePeak( tofds.binCenters(), 10.0, 4.0, 102.4, 3.8)
    d2 = NdArray( dtype, d2List)
    err2 = d2.copy()
    err2.sqrt()

    from histogram.NdArrayDataset import Dataset
    ds2 = Dataset( storage=d2, shape=[d2.size()])
    errds2 = Dataset( storage=err2, shape=[d2.size()])
    from histogram.ins.MonitorData import MonitorData
    m2 = MonitorData( intensity=ds2, intensityError=errds2, intensityUnit="",
                      tof=tofds, tofUnit="second", position=[10.0,0.0,0.0], cartesianPosition=[10.0,0.0,0.0],
                      monitor=None, name="monitor 2")

    
    # construct "monitor 3"
    d3List = simplePeak( tofds.binCenters(), 90.0, 7.2, 12.4, 1.8)
    d3 = NdArray( dtype, d3List)
    err3 = d2.copy()
    err3.sqrt()

    ds3 = Dataset( storage=d3, shape=[d3.size()])
    errds3 = Dataset( storage=err3, shape=[d3.size()])
    
    m3 = MonitorData( intensity=ds3, intensityError=errds3, intensityUnit="",
                      tof=tofds, tofUnit="s", position=[90.0,0.0,0.0],
                      cartesianPosition=[90.0, 0.0, 0.0],
                      monitor=None, name="monitor 3")


    solver = IncidentEnergySolver()

    energy = solver.solve( m2, m3, [11, 5.0, 90.0, 5.0], [75, 5.0, 10.0, 1.0])

    log("energy is %s" % energy)
    
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


target = "IncidentEnergySolver"
import journal

log = journal.info( target).log

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: histCompatTest_IncidentEnergySolver.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file

