#!/usr/bin/env python
# Copyright (c) 2005 Timothy M. Kelley all rights reserved

 utilities

target = "vectorCompat"   # name of package being tested

log = utilities.picklog( target)

def runTests( **kwds):

    # do not alter the next statement, or py_test.py may not work 
    testmods = [
        "MonitorNormalizer",
        "MultScalarErrorProp",
        "DivScalarErrorProp",
        "SimpleFitter",
        "He3DetEffic",
        "AddErrorProp",
        "SubtractErrorProp",
        "MultErrorProp",
        "DivErrorProp",
        "AddScalarErrorProp",
        "EBinCalcor",
        "ERebinAllInOne"# <eol>
        ]  # list of strings, one per module
    
    allPassed = True
    records = {}

    for mod in testmods:
        exec 'from vectorCompatTest_%s import run' % mod
        utilities.preReport( log, mod, "")
        passed = run( noGraph=True)
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
__id__ = "$Id: run_vectorCompatTests.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file
