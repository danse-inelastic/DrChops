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


from VanadiumReduction import VanadiumReduction
from Job import Job

from DbObject import DbObject
class ReductionToMslice(DbObject):

    name = 'reductionstomslice'

    import pyre.db

    main_runno = pyre.db.varchar( name = 'main_runno', length = 128)
    mt_runno = pyre.db.varchar( name = 'mt_runno', length = 128)
    mtratio = pyre.db.real( name = 'mtratio', default = 0.9 )
    
    E_params = pyre.db.doubleArray( name = 'E_params', default = [-60,60,1] )
    tof_params = pyre.db.doubleArray( name = 'tof_params', default = [3000,6000,5] )
    Ei = pyre.db.real( name = 'Ei', default = 100 )

    calibration = pyre.db.reference(name='calibration', table = VanadiumReduction)

    job = pyre.db.reference(name='job', table = Job)



# version
__id__ = "$Id$"

# End of file 
