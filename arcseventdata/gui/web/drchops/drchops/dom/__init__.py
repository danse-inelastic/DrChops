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


def alltables():
    from _all_tables import tables
    return tables


def reductiontables():
    from _reductions import all
    return all()


def set_idgenerator( generator ):
    import idgenerator
    idgenerator.generator = generator
    return


def register_alltables():
    tables = alltables()
    from registry import tableRegistry
    for t in tables: tableRegistry.register( t )
    return


# version
__id__ = "$Id$"

# End of file 
