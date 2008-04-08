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

## \package reduction.pyre.inventory
## reduction-specific pyre inventory tools


from pyre.inventory import *


def numberlist(name, **kwds):
    from properties.NumberList import NumberList
    return NumberList(name, **kwds)



# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Thu Jul 27 09:23:16 2006

# End of file 
