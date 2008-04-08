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
debug = journal.debug("testLrmecsReductionApp")


def test(appName = "LrmecsReductionApp", caseName = "fulltest"):
    from shutil import copyfile
    copyfile( "%s.pml.%s" % (appName, caseName),  "%s.pml"%appName)
    
    checkDataFiles()

    os.system("%s.py"%appName)
    
    compareS( "spehist.pkl", "spehist.pkl.%s"%caseName, "S(phi,E)" )
    compareS( "sqehist.pkl", "sqehist.pkl.%s"%caseName, "S(Q,E)" )

    debug.log("%s of %s done." % (caseName, appName))
    print "%s of %s passed" % (caseName, appName)
    return


from compareS import compareS




def checkDataFiles():
    files = [
        "4849",
        "4779",
        "4844",
        ]
    
    dataDir = os.path.join( "..", '..',  "ins-data", "Lrmecs")
    
    for f in files:
        f = os.path.join( dataDir, f )
        if os.path.exists(  f  ):
            if not os.path.isfile( f ): raise "%s exists but is not a file" % f
            continue
        continue
    return



# version
__id__ = "$Id: LrmecsReductionApp.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
