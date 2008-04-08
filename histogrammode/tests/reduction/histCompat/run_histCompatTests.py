#!/usr/bin/env python
# Copyright (c) 2005 Timothy M. Kelley all rights reserved

import ARCSTest.utilities as utilities

target = "histCompat"   # name of package being tested

log = utilities.picklog( target)

def runTests( **kwds):

    # do not alter the next statement, or py_test.py may not work 
    testmods = [
        "IncidentEnergySolver",
#        "AddErrorProp",
#        "SubtractErrorProp",
#        "MultErrorProp",
#        "DivErrorProp",
#        "AddScalarErrorProp",
#        "MultScalarErrorProp",
#        "DivScalarErrorProp",
#        "HistogramAdder",
#        "HistogramSubtracter",
#        "HistogramMultiplier",
        #"HistogramDivider",
        "SimpleFitter",
#        "HistogramAverager",
        "ARCSDetCalibCalcor",
        "EBinCalcor",
        "ERebinAllInOne",
#        "HistogramScalarAdder",
        "MonitorNormalizer"# <eol>
        ]  # list of strings, one per module
    
    allPassed = True
    records = {}

    for mod in testmods:
        exec 'from histCompatTest_%s import run' % mod
        utilities.preReport( log, mod, "")
        passed = run()
        if passed:
            records[mod] = 'PASSED'
        else:
            records[mod] = 'FAILED'
        utilities.postReport( log, mod, "", passed)
        allPassed = allPassed and passed

    if allPassed:
        log( "All Python tests of %s PASSED" % target)
    else:
        log( "Some/all Python tests of %s FAILED" % target)

    _summarize( records)

    return allPassed


def _summarize( records):
    print '*'*80
    print "Test summary:"
    keys = records.keys()
    keys.sort()
    for key in keys:
        print "Test of %s %s" % (key, records[key])
    print "End of test"
    return


if __name__ == '__main__':
    import journal
    journal.info( target).activate()
    journal.debug( target).activate()
    runTests()


# version
__id__ = "$Id: run_histCompatTests.py 1000 2006-07-20 06:52:48Z linjiao $"

# End of file
