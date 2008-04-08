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


import os


import journal
debug = journal.debug("testPharosReductionApp")


def test(cmd, appName = "PharosReductionApp", caseName = "fulltest"):
    from shutil import copyfile
    copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)

    getDataFiles()

    os.system( cmd )
    
    compareS( "spe.pkl", "spe.pkl.%s"%caseName, "S(phi,E)" )
    compareS( "sqe.pkl", "sqe.pkl.%s"%caseName, "S(Q,E)" )

    debug.log("%s of %s done." % (caseName, appName))
    print "%s of %s passed" % (caseName, appName)
    return


from compareS import compareS




def getDataFiles():
    files = [
        "Pharos_318.nx.h5",
        "Pharos_342.nx.h5",
        "Pharos_351.nx.h5",
        "Pharos_3322.nx.h5",
        "Pharos_3325.nx.h5",
        "Pharos_552.nx.h5",
        ]
    
    dataDir = os.path.join("..", '..', "ins-data", "Pharos")
    
    for f in files:
        f = os.path.join( dataDir, f )
        if os.path.exists(  f  ):
            if not os.path.isfile( f ): raise "%s exists but is not a file" % f
            continue
        gunzip( f+".gz" )
        continue
    return


def gunzip( zipfile ):
    print "about to unzip %s" % zipfile
    if os.path.exists(zipfile):
        cmd = "gunzip %s" % zipfile
        print "execute %s" % cmd
        if os.system (cmd):
            raise "automatic unzip of file %s failed. please do it "\
                  "manually before running this test" % zipfile
        pass
    else: raise OSError , "file %s does not exist" % zipfile
    return



import unittest

class Tests(unittest.TestCase):

    def __init__(self, *args, **kwds):
        unittest.TestCase.__init__(self, *args, **kwds)
        getDataFiles()
        return


    def _test(self, case):
        cmd =  '''rsh -. n01 "PharosReductionApp_Parallel.py -launcher.nodelist=1 -launcher.nodegen='n%02d:4' -launcher.nodes=4 " '''
        global test
        test( cmd, 'PharosReductionApp', caseName = case )
        return
    

    def test1(self):
        "PharosReductionApp: full reduction test"
        self._test("342_318_351")
        return


    def test2(self):
        "PharosReductionApp: full reduction test with new data format"
        self._test("3322_552_3325")
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
