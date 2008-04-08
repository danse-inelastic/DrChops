#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                   (C) Copyright 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""This script is to create standard pkl files to be compared to
should not be used very often. only use it a major change has been
made and reduced S(phi,E) or S(Q,E) changes. Those changes must
be validated carefully before we run this script. 
"""

import os


import journal
debug = journal.debug("testPharosReductionApp")


def test(appName = "PharosReductionApp", caseName = "fulltest"):
    from shutil import copyfile
    copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)

    getDataFiles()

    os.system("%s.py"%appName)
    
    copyfile( "spe.pkl", "spe.pkl.%s"%caseName )
    copyfile( "sqe.pkl", "sqe.pkl.%s"%caseName )

    return


def getDataFiles():
    files = [
        "Pharos_318.nx.h5",
        "Pharos_342.nx.h5",
        "Pharos_351.nx.h5",
        "Pharos_3322.nx.h5",
        "Pharos_3325.nx.h5",
        "Pharos_552.nx.h5",
        ]
    
    dataDir = os.path.join('..', '..', "ins-data", "Pharos")
    
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


def plot(x, y, z, min = None, max = None):
    from reduction.utils.plotter import pylabPlotter2D as pl
    pl.plot_(x,y,z, min = min, max = max)
    return


from histogram.data_plotter import _guessMax as guessMax



def main():
    debug.activate()
    for name in ['342_318_351', '3322_552_3325']:
        test(caseName = name)
        continue
    print "test standard generated"
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id: PharosReductionApp.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
