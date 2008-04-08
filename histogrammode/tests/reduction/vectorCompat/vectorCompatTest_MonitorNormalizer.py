#!/usr/bin/env python
# Copyright (c) 2004 Timothy M. Kelley all rights reserved


import os
curdir = os.path.split( __file__ ) [0]
if curdir == "" or curdir ==".": curdir = os.environ['PWD']

nx5testfile = os.path.join( curdir, 'inputs', 'NXtest.nx5.test' )


aspects = [
    "instantiate/initialize",
    "determineNorm()",
    "norm()",
    "sigma_norm2",
    "normalize(), no errors",
    "normalize(), check only errors",
    "normalize(), check both",
    "normalize(), different outputs, check both",
    ]


def test_0( **kwds):

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    return True

    
def test_1( **kwds):

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    mn.determineNorm( monData, 0, 20, dt = 0.5)
    answer = 105.0; sigma_answer = 52.5; epsilon = 1e-20
    passed = True
    if mn._norm + epsilon < answer or mn._norm - epsilon > answer:
        passed = False
        log( "mn._norm was %s instead of %s to within %s" %
             ( mn._norm, answer, epsilon))
    if mn._sigma2 + epsilon < sigma_answer or mn._sigma2 - epsilon > sigma_answer:
        passed = False
        log( "mn._sigma2 was %s instead of %s to within %s" %
             ( mn._sigma2, sigma_answer, epsilon))
    return passed

    
def test_2( **kwds):

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    mn.determineNorm( monData, 0, 20, dt = 0.5)
    answer = 105.0; epsilon = 1e-20
    passed = True
    norm = mn.norm()
    if norm + epsilon < answer or norm - epsilon > answer:
        passed = False
        log( "norm() was %s instead of %s to within %s" %
             ( norm, answer, epsilon))
    return passed

    
def test_3( **kwds):

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    mn.determineNorm( monData, 0, 20, dt = 0.5)
    answer = 52.5; epsilon = 1e-20
    passed = True
    norm = mn.sigma_norm2()
    if norm + epsilon < answer or norm - epsilon > answer:
        passed = False
        log( "sigma_norm2() was %s instead of %s to within %s" %
             ( norm, answer, epsilon))
    return passed

    
def test_4( **kwds):

    length = 20

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    mn.determineNorm( monData, 0, 20, dt = 0.5)

    from stdVector import vector
    dataset = vector( 6, 20, 1.0)

    mn.normalize( dataset=dataset, outputDataset=dataset, error=None,
                  outputError=None, tempVector=None)

    expected = [1.0/105.0 for i in range(length)]
    epsilon = 1e-20
    passed = utilities.compareFPLists( dataset.asList(), expected,
                                       epsilon, log)
    return passed

    
def test_5( **kwds):

    length = 20

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    mn.determineNorm( monData, 0, 20, dt = 0.5)

    from stdVector import vector
    dataset = vector( 6, 20, 2.0)
    error = vector( 6, 20, 3.0)
    a = mn.norm()
    sigma_a2 = mn.sigma_norm2()
    log("mn.norm() = %s, sigma_norm2 = %s" % ( a, sigma_a2))

    expected = [1/(a**4)*sigma_a2*4.0 + 1/(a**2)*3.0 for i in range( 20)]

    mn.normalize( dataset=dataset, outputDataset=dataset, error=error,
                  outputError=error, tempVector=None)

#    expected = [1.0/105.0 for i in range(length)]
    epsilon = 1e-20
    passed = utilities.compareFPLists( error.asList(), expected,
                                       epsilon, log)
    return passed

    
def test_6( **kwds):

    length = 20

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    mn.determineNorm( monData, 0, 20, dt = 0.5)

    from stdVector import vector
    dataset = vector( 6, 20, 2.0)
    error = vector( 6, 20, 3.0)
    a = mn.norm()
    sigma_a2 = mn.sigma_norm2()
    log("mn.norm() = %s, sigma_norm2 = %s" % ( a, sigma_a2))

    expected_errs = [1/(a**4)*sigma_a2*4.0 + 1/(a**2)*3.0 for i in range( 20)]

    mn.normalize( dataset=dataset, outputDataset=dataset, error=error,
                  outputError=error, tempVector=None)

    expected_data = [2.0/105.0 for i in range(length)]
    epsilon = 1e-20
    passed_errs = utilities.compareFPLists( error.asList(), expected_errs,
                                            epsilon, log)

    log("errors okay? %s" % passed_errs)
    
    passed_data = utilities.compareFPLists( dataset.asList(), expected_data,
                                            epsilon, log)
    log("data okay? %s" % passed_data)

    return passed_errs and passed_data

    
def test_7( **kwds):

    length = 20

    import nx5.file
    f = nx5.file.file(nx5testfile, 'r')
    selector = f.selector()
    selector.select( '/entry/r8_data')
    
    from nx5.file.VectorReader import Reader
    reader = Reader()
    monData = reader.read( selector)

    from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
    mn = MonitorNormalizer()

    mn.determineNorm( monData, 0, 20, dt = 0.5)

    from stdVector import vector
    dataset = vector( 6, 20, 2.0)
    outdata = vector( 6, 20, 0.0)
    error = vector( 6, 20, 3.0)
    outerror = vector( 6, 20, 0.0)
    
    a = mn.norm()
    sigma_a2 = mn.sigma_norm2()
    log("mn.norm() = %s, sigma_norm2 = %s" % ( a, sigma_a2))

    expected_errs = [1/(a**4)*sigma_a2*4.0 + 1/(a**2)*3.0 for i in range( 20)]
    expected_data = [2.0/105.0 for i in range(length)]

    mn.normalize( dataset=dataset, outputDataset=outdata, error=error,
                  outputError=outerror, tempVector=None)

    epsilon = 1e-20
    passed_outerrs = utilities.compareFPLists( outerror.asList(),
                                               expected_errs,
                                               epsilon, log)

    log("output errors okay? %s" % passed_outerrs)
    
    passed_outdata = utilities.compareFPLists( outdata.asList(), expected_data,
                                               epsilon, log)
    log("output data okay? %s" % passed_outdata)

    passed_errs = utilities.compareFPLists( error.asList(),
                                            [3.0 for i in range(20)],
                                            epsilon, log)

    log("input errors okay? %s" % passed_errs)
    
    passed_data = utilities.compareFPLists( dataset.asList(),
                                            [2.0 for i in range(20)],
                                            epsilon, log)
    log("input data okay? %s" % passed_data)

    return passed_outerrs and passed_outdata and passed_errs and passed_data

    
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

target = "MonitorNormlizer"

log = utilities.picklog( target)

if __name__ == '__main__':
    import journal
    info = journal.info( target)
    info.activate()
    
    run()

# version
__id__ = "$Id: vectorCompatTest_MonitorNormalizer.py 1099 2006-08-13 03:03:00Z linjiao $"

# End of file

