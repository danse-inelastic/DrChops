#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os

def getTests( path ):
    "get all test scripts under path. no recurse"
    files = os.listdir( path )

    tests = []
    for f in files:
        if f.endswith("TestCase.py"): tests.append( os.path.join( path, f ) )
        continue
    return tests


def getTestR( path ):
    "get all test scripts under path. recurse"
    entries = os.listdir( path )
    ret = getTests( path )

    for entry in entries:
        p = os.path.join( path, entry )
        if os.path.isdir( p ):
            ret += getTestR( p )
            pass
        continue
    return ret


def run( tests, excludedDir = ['obsolete'] ):
    failed = [ ]
    for t in tests:
        path, f = os.path.split( t )

        bypass = False
        for d in excludedDir:
            if d in path: bypass = True; break
            pass

        if bypass : continue
        
        if rununittest( path, f ) : failed.append( t )
        continue
    return failed


def rununittest( path, f ):
    curdir = _curdir()
    tmpfile = os.path.join( curdir, 'testresult' )
    cmd = "cd %s && python %s 2>&1 | tee %s && cd -" % (path, f, tmpfile)
    os.system(cmd)
    output = open( tmpfile ).read()
    if output.find( 'FAILED' ) != -1: return 1
    return 0


def _curdir():
    #get current directory
    curdir = os.path.split( __file__ ) [0]
    if curdir == "": curdir = "."
    return os.path.abspath( curdir )


def help():
    return '''
runall.py
runall.py -N
'''


def warning():
    print ' *** This test scripts use some nasty ticks. If tests has interactive parts, it is better not to use this script'
    return


def main():
    warning()
    import sys
    argv = sys.argv
    if len(argv) > 2:
        print help()
        return
    if len(argv) == 2:
        if argv[1] == '-N':
            tests = getTests( _curdir() )
            pass
        print help()
        return
    else:
        tests = getTestR( _curdir() )
        pass
    failed = run( tests )
    
    print "Run %s tests, %s failed. \nFailed tests: %s" % (
        len(tests), len(failed), failed )
    return


if __name__ == "__main__" : main()


# version
__id__ = "$Id$"

# End of file 
