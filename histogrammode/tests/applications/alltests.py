#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os


## import unittest as ut


## def addTestMethod( klass, path):
##     import sys
##     save = sys.path
##     sys.path = [path] + sys.path
##     import alltests
##     reload (alltests)
##     def f(self):
##         os.chdir( path )
##         r = ut.TextTestRunner(verbosity=2).run(alltests.alltests)
##         self.assert_( r.wasSuccessful() )
##         return
##     name = os.path.split( path )[1]
##     casename = name.replace(' ', '_').replace('-', '_')
##     setattr( klass, "test%s" % casename, f)
##     sys.path = save
##     return
    

## def makeTestCase(dir):
##     class TestCase(ut.TestCase): pass
##     for subdir in os.listdir( dir ):
##         path = os.path.join( dir, subdir )
##         if os.path.isdir( path ):
##             addTestMethod( TestCase, path )
##         continue
##     return TestCase


## def suite():
##     curdir = os.path.abspath( os.curdir )
##     TC = makeTestCase( curdir )
##     s = ut.makeSuite( TC )
##     return s

## def main():
##     ut.TextTestRunner(verbosity=2).run(suite())
##     return


def run( dir ):
    exe = os.path.join( os.curdir, "alltests.py" )
    for subdir in os.listdir( dir ):
        path = os.path.join( dir, subdir )
        if os.path.isdir( path ):
            cmd = "cd %s && %s && cd .." % (path, exe)
            print cmd
            os.system( cmd )
            pass
        continue
    return
    

def main():
    run( os.curdir )
    return


if __name__ == "__main__" : main()

# version
__id__ = "$Id$"

# End of file 
