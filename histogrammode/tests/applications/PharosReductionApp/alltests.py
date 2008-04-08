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
if curdir == "": curdir = os.environ['PWD']

#get all files
files = os.listdir( curdir )

#get names of all test cases
tests = []
for f in files:
    if f.endswith("TestCase.py"): tests.append( f.rstrip('.py') )
    continue



#print tests

#make a list of test suites
allsuites = []
for test in tests:
    print test
    testmodule = __import__( test )
    print testmodule
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
__id__ = "$Id: alltests.py 1089 2006-08-11 17:45:53Z linjiao $"

# End of file 
