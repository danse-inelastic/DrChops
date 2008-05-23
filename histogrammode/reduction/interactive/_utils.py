#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os
def curdir():
    f = __file__
    d = os.path.dirname(f)
    if d == '': d = '.'
    return d


def getModules( ):
    "get and import a list of python modules under the current directory"
    rt = []
    path = curdir()
    for entry in os.listdir( path ):
        f = os.path.join( path, entry )
        #print f
        if os.path.isdir( f ): continue
        modulename, ext = os.path.splitext( entry )
        if modulename.startswith( '_' ): continue
        if ext not in [".pyc", '.py'] : continue
        exec "import %s as m" % (modulename,)
        if m not in rt: rt.append( m )
        continue
    return rt



def test_getModules():
    print getModules( )
    return 


def main():
    test_getModules()
    return 

if __name__ == "__main__": main()



# version
__id__ = "$Id$"

# End of file 
