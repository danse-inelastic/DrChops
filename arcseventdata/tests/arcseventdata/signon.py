#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

if __name__ == "__main__":

    import arcseventdata
    from arcseventdata import arcseventdata as arcseventdatamodule

    print "copyright information:"
    print "   ", arcseventdata.copyright()
    print "   ", arcseventdatamodule.copyright()

    print
    print "module information:"
    print "    file:", arcseventdatamodule.__file__
    print "    doc:", arcseventdatamodule.__doc__
    print "    contents:", dir(arcseventdatamodule)

    print
    print arcseventdatamodule.hello()

# version
__id__ = "$Id$"

#  End of file 
