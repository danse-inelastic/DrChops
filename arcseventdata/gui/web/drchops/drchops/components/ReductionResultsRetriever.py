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
        calibration = reduction
        calijob = calibration.job.dereference(self.director.db)
        calijobdir = _jobpath(calijob)
        calibrationh5 = os.path.join(calijobdir, 'calibration.h5')
        maskh5 = os.path.join(calijobdir, 'mask.h5')
        return calibrationh5, maskh5


from Job import jobpath as _jobpath
import os

# version
__id__ = "$Id$"

# End of file 
