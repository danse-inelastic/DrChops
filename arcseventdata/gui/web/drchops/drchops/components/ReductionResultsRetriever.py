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

def retrieve(reduction, director):
    return ReductionResultsRetriever(director)(reduction)


class ReductionResultsRetriever:

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
        files = [
            'calibration.h5',
            'mask.h5',
            ]
        path = resultspath(reduction)
        ret = _findReductionResults(path, files)
        if ret: return ret

        # try to find from job
        job_ref = reduction.job
        if job_ref is None: return
        job = job_ref.dereference(self.director.db)
        jobpath = _jobpath(job)
        ret = _findReductionResults(jobpath, files)
        if ret is None: return
        
        # move results from job directory to reduction directory
        _moveFiles(jobpath, files, path)
        ret = _findReductionResults(path, files)
        if ret is None: raise RuntimeError
        return ret


def _findReductionResults(path, files):
    paths = []
    for f in files:
        p = os.path.join(path, f)
        if not os.path.exists(p): return
        paths.append( os.path.abspath(p) )
        continue
    return paths


def _moveFiles(source, files, dest):
    for f in files:
        old = os.path.join(source, f)
        new = os.path.join(dest,f)
        os.rename(old, new)
        continue
    return


reduction_results_root_dir = 'reduced'
def resultspath(reduction):
    path = os.path.join( reduction_results_root_dir, reduction.__class__.__name__,
                         reduction.id )
    if os.path.exists(path) and not os.path.isdir(path):
        raise IOError, '%s is not a directory' % path
    if not os.path.exists(path):
        os.makedirs( path )
    return path


from Job import jobpath as _jobpath
import os

# version
__id__ = "$Id$"

# End of file 
