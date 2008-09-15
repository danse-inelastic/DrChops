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


class ReductionJobBuilder:

    def __init__(self, director):
        self.director = director
        return

    
    def __call__(self, reduction):
        return self.dispatch(reduction)


    def dispatch(self, reduction):
        typename = reduction.__class__.__name__
        handler = getattr( self, 'on%s' % typename)
        return handler( reduction )


    def onVanadiumReduction(self, reduction):
        job = self._newjob()
        jobpath = _jobpath( job )
        self._prepareJobpath(jobpath)
        
        runno = reduction.runno
        E_params = reduction.E_params
        Ei = reduction.Ei
        
        rundir = _rundir(runno)

        cmds = ['#!/usr/bin/env sh']
        cmds.append( 'ARCSReduceVanadiumData.py -v %r -E %s -I %s -mpirun.nodes=8' % (
            rundir, ','.join( [ str(p) for p in E_params] ), Ei) )

        makeJobScript(jobpath, '\n'.join(cmds) )

        job.computation = reduction
        self.director.clerk.updateRecord(job)
        
        reduction.job = job
        self.director.clerk.updateRecord(reduction)
        return job


    def onReductionToMslice(self, reduction):
        job = self._newjob()
        jobpath = _jobpath( job )
        self._prepareJobpath(jobpath)
        
        main_runno = reduction.main_runno
        mt_runno = reduction.mt_runno
        mtratio = reduction.mtratio
        E_params = reduction.E_params
        tof_params = reduction.tof_params
        Ei = reduction.Ei

        #calibration results
        calibration = reduction.calibration.dereference(self.director.db)
        from ReductionResultsRetriever import retrieve
        calibrationh5,maskh5 = retrieve(calibration, director)
        
        main_rundir = _rundir(main_runno)
        mt_rundir = _rundir(mt_runno)

        cmds = ['#!/usr/bin/env sh']
        cmds.append( 'ARCSReduceToMsliceFiles.py -r %r -M %r -R %s -E %s -t %s -I %s --calibration=%r --mask=%r -mpirun.nodes=8' % (
            main_rundir, mt_rundir, mtratio,
            ','.join( [ str(p) for p in E_params] ),
            ','.join( [ str(p) for p in tof_params] ),
            Ei, calibrationh5, maskh5)
                     )

        makeJobScript(jobpath, '\n'.join(cmds) )

        job.computation = reduction
        self.director.clerk.updateRecord(job)
        
        reduction.job = job
        self.director.clerk.updateRecord(reduction)
        return job


    def _prepareJobpath(self, path):
        import os
        #make a symbolic link to ARCS.xml
        origin = '/SNS/users/lj7/reduction/runs/88/ARCS.xml' 
        cmd = 'ln -s %s %s/ARCS.xml' % (origin, path)
        if os.system( cmd ): raise RuntimeError, "cmd %s failed" % cmd
        
        #make a symbolic link to pixelInfo-cache
        origin = '/SNS/users/lj7/reduction/runs/88/pixelInfo-cache'
        cmd = 'ln -s %s %s/pixelInfo-cache' % (origin, path)
        if os.system( cmd ): raise RuntimeError, "cmd %s failed" % cmd
        return


    def _newjob(self):
        clerk = self.director.clerk
        job = clerk.newJob()
        job.state = 'created'
        clerk.updateRecord(job)
        return job


from misc import find_arcs_run_dir as _rundir
from Job import makeJobScript, jobpath as _jobpath
import os

# version
__id__ = "$Id$"

# End of file 
