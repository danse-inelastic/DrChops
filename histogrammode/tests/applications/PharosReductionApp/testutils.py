import os


import journal
debug = journal.debug("testPharosReductionApp")


def test(appName = "PharosReductionApp", caseName = "fulltest"):
    from shutil import copyfile
    copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)

    getDataFiles()

    os.system("%s.py"%appName)
    
    compareS( "spehist.pkl", "spehist.pkl.%s"%caseName, "S(phi,E)" )
    compareS( "sqehist.pkl", "sqehist.pkl.%s"%caseName, "S(Q,E)" )

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



