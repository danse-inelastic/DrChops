#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                   (C) Copyright 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from testutils import *

import unittest

class Tests(unittest.TestCase):

    def __init__(self, *args, **kwds):
        unittest.TestCase.__init__(self, *args, **kwds)
        getDataFiles()
        return
    

    def test2(self):
        "PharosReductionApp: full reduction test with new data format"
        global test
        test(caseName = "3322_552_3325")
        return

    pass 
        

def pysuite():
    suite1 = unittest.makeSuite(Tests)
    return unittest.TestSuite( (suite1,) )



def main():
    debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id: PharosReductionApp.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
