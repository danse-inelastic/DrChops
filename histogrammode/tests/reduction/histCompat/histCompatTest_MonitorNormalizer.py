#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved

aspects = [
    "instantiate",
    
    ]


from reduction.histCompat.MonitorNormalizer import MonitorNormalizer

def test_0( **kwds):

    normalizer = MonitorNormalizer()

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



target = "MonitorNormalizer"
import journal
log = journal.info( target).log

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: histCompatTest_MonitorNormalizer.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

