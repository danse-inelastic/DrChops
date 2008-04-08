#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from dsm.Connectable import Connectable as dsmConnectable
from pyre.components.Component import Component
class Connectable( Component, dsmConnectable ):

    class Inventory(Component.Inventory): pass

    def __init__(self, *args, **kwds):
        Component.__init__(self, *args, **kwds)
        dsmConnectable.__init__( self )
        return


    def __str__(self): return self.name

    pass # end of Connectable


# version
__id__ = "$Id$"

# End of file 
