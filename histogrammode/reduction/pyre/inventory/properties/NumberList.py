#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao  Lin
#                      California Institute of Technology
#                        (C) 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from pyre.inventory.properties.List import List


class NumberList(List):


    def __init__(self, name, default=[], meta=None, validator=None):
        List.__init__(self, name, default, meta, validator)
        return


    def _cast(self, text):
        if isinstance(text, basestring):
            l = List._cast(self, text)
        elif isinstance(text, list) or isinstance(text,tuple):
            l = text
        else:
            raise TypeError, "cannot convert %r(%s) to a list" % (
                text, type(text) )
        if len(l) == 1 and l[0] == '': return []
        try:
            return [ _eval(item) for item in l ]
        except Exception, msg:
            raise TypeError("property '%s': could not convert '%s' to a number list because %s" % (self.name, text, msg))
    


def _eval(s):
    'recursively evaluate until we got a number'
    if isinstance(s, int) or isinstance(s, float):
        return s
    else:
        return _eval(eval(s))


# version
__id__ = "$Id: NumberList.py 18 2005-06-11 04:00:21Z linjiao $"

# End of file 
