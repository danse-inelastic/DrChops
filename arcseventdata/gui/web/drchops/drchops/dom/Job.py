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

from registry import tableRegistry


from DbObject import DbObject
class Job(DbObject):

    name = 'jobs'

    import pyre.db

    id_incomputingserver = pyre.db.varchar(name="id_incomputingserver", length=100)
    id_incomputingserver.meta['tip'] = "the id of this job when submitted to the computing server. this is given by the computing server."

    timeCompletion = pyre.db.varchar(name='timeCompletion', length = 64)
    timeCompletion.meta['tip'] = 'time left to completion'
    
    timeStart = pyre.db.varchar(name='timeStart', length = 64)
    timeStart.meta['tip'] = 'the time the job started'
    
    numprocessors = pyre.db.integer(name='numprocessors', default = 1)
    numprocessors.meta['tip'] = 'the number of processors this job uses'

    id_incomputingserver = pyre.db.varchar(name="id_incomputingserver", length=100)
    id_incomputingserver.meta['tip'] = "the id of this job when submitted to the computing server. this is given by the computing server."

    owner = pyre.db.varchar( name = 'owner', length = 30 )
    owner.meta['tip'] = 'the owner of this job'

    state = pyre.db.varchar( name = 'state', length = 64 )
    # state:-1
    #   - created: just created. has not been submitted
    #   - submitted
    #   - running
    #   - onhold
    #   - finished

    output = pyre.db.varchar(name = 'output', length = 2048)
    error = pyre.db.varchar(name = 'error', length = 2048)
    
    exit_code = pyre.db.integer(name = 'exit_code', default = -1)

    computation = pyre.db.versatileReference(
        name = 'computation', tableRegistry = tableRegistry)


# version
__id__ = "$Id$"

# End of file 
