#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                                Max Kresch
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
        checkDataFiles()
        return
    

    def test2(self):
        "LrmecsReductionApp: main 4849, calib 4779, mt 4844"
        global test
        test(caseName = "4849_4779_4844")
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
__id__ = "$Id: LrmecsReductionApp.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
