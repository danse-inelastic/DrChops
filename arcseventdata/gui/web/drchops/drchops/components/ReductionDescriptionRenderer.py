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

def describe(reduction, director):
    return ReductionDescriptionRenderer(director)(reduction)


class ReductionDescriptionRenderer:

    def __init__(self, director):
        self.director = director
        return

    
    def __call__(self, reduction):
        self._ret = ''
        return self.dispatch(reduction)


    def dispatch(self, reduction):
        typename = reduction.__class__.__name__
        self._ret += '%s #%s, ' % (typename, reduction.id) 
        handler = getattr( self, 'on%s' % typename)
        handler( reduction )
        return self._ret


    def onVanadiumReduction(self, reduction):
        text = [
            'run #%s' % reduction.runno,
            'Ei=%s' % reduction.Ei,
            ]
        self._ret += ', '.join( text )
        return


    def onReductionToMslice(self, reduction):
        director = self.director
        db = director.db
        text = [
            'main run #%s' % reduction.main_runno,
            'mt run #%s' % reduction.mt_runno,
            ]
        calibration_ref = reduction.calibration
        if calibration_ref:
            text.append(
                'calibration run #%s' % reduction.calibration.dereference(db).runno)
        text += [
            'mtratio=%s' % reduction.mtratio,
            'Ei=%s' % reduction.Ei,
            ]
        job_ref = reduction.job
        if job_ref is None:
            text.append( 'Not started' )
        else:
            job = job_ref.dereference(db)
            text.append( job.state )
        self._ret += ', '.join( text )
        return


from Job import jobpath as _jobpath
import os

# version
__id__ = "$Id$"

# End of file 
