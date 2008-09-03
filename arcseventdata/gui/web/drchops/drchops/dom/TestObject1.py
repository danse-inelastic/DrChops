# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from DbObject import DbObject

class TestObject1(DbObject):

    name = 'test1'

    import pyre.db

    text1 = pyre.db.varchar( name = 'text1', length = 128, default = "abcdefg" )
    text1.meta['tip'] = 'text1'

    text2 = pyre.db.varchar( name = 'text2', length = 128, default = "abcdefg" )
    text2.meta['tip'] = 'text2'


# version
__id__ = "$Id$"

# End of file 
