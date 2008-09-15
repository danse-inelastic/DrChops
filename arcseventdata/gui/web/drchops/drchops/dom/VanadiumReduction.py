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


from Job import Job

from DbObject import DbObject
class VanadiumReduction(DbObject):

    name = 'vanadiumreductions'

    import pyre.db

    runno = pyre.db.varchar( name = 'runno', length = 128)
    E_params = pyre.db.doubleArray( name = 'E_params', default = [-60,60,1] )
    Ei = pyre.db.real( name = 'Ei', default = 100 )

    job = pyre.db.reference(name='job', table = Job)


def inittable(db):
    def new(id, runno, E_params, Ei):
        r = VanadiumReduction()
        r.runno = runno
        r.Ei = Ei
        r.E_params = E_params
        r.id = id
        return r

    db.insertRow( new( new_id(), 128, [-60,60,1], 100 ) )
    return
    

def new_id():
    from idgenerator import generator
    return generator()


# version
__id__ = "$Id$"

# End of file 
