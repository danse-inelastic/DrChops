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


def check(job, director):
    if job.state in ['finished', 'failed', 'terminated']:
        # should have no need to update
        return
    
    schedulerf = schedulerfactory('slurm')
    partition = 'arcs'
    node = 'arcs2'

    path = jobpath(job)
    prefix = 'cd %s' % path
    
    scheduler = schedulerf(
        spawn,
        prefix = prefix, partition = partition, node = node )

    from drchops.clusterscheduler.exceptions import UnableToObtainStatus
    try:
        status = scheduler.status( job.id_incomputingserver )
    except UnableToObtainStatus:
        # the job is probably terminated
        status = {'state': 'terminated'}
        
    for k, v in status.iteritems():
        setattr( job, k, v )
        continue

    director.clerk.updateRecord(job)
    return


def submit(job, director):
    schedulerf = schedulerfactory('slurm')
    partition = 'arcs'
    node = 'arcs2'

    path = jobpath(job)
    prefix = 'cd %s' % path
    
    scheduler = schedulerf(
        spawn,
        prefix = prefix, partition = partition, node = node )
    
    global scriptname
    id = scheduler.submit(scriptname)
    job.id_incomputingserver = id
    job.state = 'submitted'

    director.clerk.updateRecord(job)
    return job


def schedulerfactory( schedulername ):
    '''obtain scheduler factory for the given scheduler name
    Eg: schedulerfactory( 'spurm' )
    '''

    if schedulername in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from drchops.clusterscheduler import scheduler as factory
    try: scheduler = factory( schedulername )
    except: raise NotImplementedError, 'scheduler %r' % schedulername
    return scheduler


scriptname = 'run.sh'
def makeJobScript( path, content ):
    f = open(os.path.join(path, scriptname), 'w')
    f.write( content )
    return


jobdirroot = 'jobs'
def jobpath(job):
    import os
    path = os.path.join(jobdirroot, job.id)
    if os.path.exists(path) and not os.path.isdir(path):
        raise IOError, '%s is not a directory' % path
    if not os.path.exists(path):
        os.makedirs( path )
    return path


import os
from drchops.clusterscheduler.spawn import spawn



# version
__id__ = "$Id$"

# End of file 
