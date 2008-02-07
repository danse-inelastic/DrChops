#!/usr/bin/env python

# This script convert a pickle file containing a numpy array to a binary file
# readable by c code


def toString( array ):
    from numpy import tostring
    array.shape = -1,
    return tostring( array )


def run( pklfn, binfn):
    from pickle import load
    array = load( open(pklfn) )
    s = array.tostring()

    open(binfn, 'wb').write( s )
    return


def help():
    msg = """numpyarray2binary.py pklfilename binfilename"""
    print msg
    return


def main():
    import sys
    if len(sys.argv) != 3: help(); exit(1)
    
    argv = sys.argv
    pklfn = argv[1]
    binfn = argv[2]
    
    run(pklfn, binfn)
    return


if __name__ == '__main__': main()

