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

#get current directory
curdir = os.path.split( __file__ ) [0]
if curdir == "": curdir = "."

#get all files
files = os.listdir( curdir )

#get names of all test cases
tests = []
for f in files:
    if f.find("Parallel")!=-1: continue
    if f.endswith("TestCase.py"): tests.append( f.rstrip('.py') )
    continue


#print tests
import sys
if '' not in sys.path: sys.path = [''] + sys.path

#make a list of test suites
allsuites = []
for test in tests:
    testmodule = __import__( test )
    suite = testmodule.pysuite()
    allsuites.append( suite )
    continue


import unittest
alltests = unittest.TestSuite( allsuites )


def main():
    #run test
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == "__main__": main()


# version
__id__ = "$Id: alltests.py 1361 2007-07-28 02:49:43Z linjiao $"

# End of file 
