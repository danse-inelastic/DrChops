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
class Measurement(DbObject):

    name = 'measurements'

    import pyre.db

    main = pyre.db.varchar( name = 'main', length = 128)
    mt = pyre.db.varchar( name = 'mt', length = 128)
    calib = pyre.db.varchar( name = 'calib', length = 128)


# version
__id__ = "$Id$"

# End of file 
