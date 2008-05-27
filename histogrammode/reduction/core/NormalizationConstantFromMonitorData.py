#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractNormalizationCalculator import AbstractNormalizationCalculator as base
from reduction import units
microsecond = units.time.microsecond


class NormalizationConstantFromMonitorData(base):


    def __init__(self, monitorId = 0, tofStart = 3000*microsecond, tofEnd = 6000*microsecond):
        '''NormalizationConstantFromMonitorData( monitorId, tofStart, tofEnd)
        
        monitorId: id of the monitor where neutron counts are integrated
        tofStart, tofEnd: tof window in which neutron counts are integrated
        '''
        self.monitorId = monitorId
        self.tofStart = tofStart
        self.tofEnd = tofEnd
        return


    def __call__(self, run):
        monitorId = self.monitorId
        start = self.tofStart
        end = self.tofEnd
        from reduction.histCompat.MonitorNormCalcor import calcor
        monData = run.getMonitorItof( monitorId )
        return calcor.calcNorm( monData, start, end )



# version
__id__ = "$Id$"

# End of file 
