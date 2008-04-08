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


import unittest


from unittest import TestCase


def addTestMethod( klass, no):
    def f(self):
        aspect, run = self.orig_tests[no]
        print self.orig_module, ':', aspect
        self.assert_( run() )
        return

    setattr( klass, "test%s" % no, f)
        

def createTestCase( originalTestModule ):

    m = __import__( originalTestModule )

    tests = []
    for i, aspect in enumerate( m.__dict__['aspects'] ):
        test_func = "test_%s" % i
        tests.append( ( aspect, m.__dict__[test_func]) )
        continue

    class NewTestCase( TestCase ): 
        orig_tests = tests
        orig_module = originalTestModule
        pass

    for i in range(len(tests)):
        addTestMethod( NewTestCase, i )
        continue

    return NewTestCase


def findTKTestModules( pre ):
    modules = []
    for entry in os.listdir( curdir ):
        if not entry.startswith( pre ): continue
        if not entry.endswith( ".py" ): continue
        if entry.find( "SimpleFitter" ) != -1: continue
        p = os.path.join( curdir, entry )
        if os.path.exists(p) and os.path.isfile(p):
            modules.append( entry[:-3] )
            pass
        continue
    return modules



def createsuites():
    modules = findTKTestModules("histCompat")
    suites = [unittest.makeSuite(createTestCase( module )) \
              for module in modules ]
    return unittest.TestSuite( suites )



alltests = createsuites()


def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: ARCSDetHistCollection_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
