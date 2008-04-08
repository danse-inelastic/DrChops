#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import os


def getTestCases( path ):

    localalltests = "alltests.py"
    p = os.path.join( path, localalltests )
    if not os.path.exists( p ) or not os.path.isfile( p ):
        raise "There is no %s in %s" % (localalltests, path)

    import sys
    orig = list ( sys.path )
    
    sys.path = [path] + sys.path
    import alltests
    reload(alltests)
    suites = alltests.alltests
    #os.chdir("..")

    sys.path = orig
    return suites



curdir = os.path.split( __file__ ) [0]
if curdir == "" or curdir ==".": curdir = os.environ['PWD']


def getAllTestCases():
    items = os.listdir( curdir )
    dirs = filter( os.path.isdir, items )
    suites = []
    for subdir in dirs:
        if subdir == ".svn" : continue
        path = os.path.join( curdir, subdir )
        suite = getTestCases( path )
        suites.append( suite )
        continue
    return suites
    

def main():
    #run test
    import unittest
    allsuites = getAllTestCases()
    alltests = unittest.TestSuite( allsuites )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": main()


# version
__id__ = "$Id: alltests.py 947 2006-05-31 01:51:51Z jiao $"

# End of file 
