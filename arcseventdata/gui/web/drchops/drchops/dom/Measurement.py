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

    main = pyre.db.str( name = 'main')
    mt = pyre.db.str( name = 'mt')
    calib = pyre.db.str( name = 'calib')


# version
__id__ = "$Id$"

# End of file 
