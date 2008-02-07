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

from pyre.inventory.Property import Property


class Tuple(Property):


    def __init__(self, name, default=None, meta=None, validator=None):
        if default is None:
            default = ()
        Property.__init__(self, name, "tuple", default, meta, validator)
        return


    def _cast(self, text):
        if isinstance(text, basestring):
            value = eval(text)
        elif isinstance(text, list):
            value = tuple(list)
        elif isinstance(text, tuple):
            pass
        else:
            raise TypeError("property '%s': could not convert '%s' to a tuple" % (self.name, text))

        if isinstance(value, tuple):
            return value
        raise TypeError("property '%s': could not convert '%s' to a tuple" % (self.name, text))

    




# version
__id__ = "$Id$"

# End of file 
