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


from Connectable import Connectable as base


class AbstractTimeIndependentBackgroundRemover(base):


    def __init__(self, name, facility = 'Time independent background remover'):
        base.__init__(self, name, facility )
        return


    sockets = {
        'in': ['mask', 'histogram'],
        'out': ['histogram'],
        }


    pass # end of AbstractTimeIndependentBackgroundRemover


# version
__id__ = "$Id$"

# End of file 
