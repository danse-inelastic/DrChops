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


## \package reduction.pyre.NormalizerUsingMonitorData
## normalize datasets using beam monitor 


from AbstractNormalizer import AbstractNormalizer as CompBase

class NormalizerUsingMonitorData(CompBase):


    """pyre component of normalizer.
    Uses monitor data to calculate normalization factor.
    """

    class Inventory(CompBase.Inventory):

        import pyre.inventory as inv

        monitorId = inv.int(
            "monitorId", default =0, validator = inv.greaterEqual(0) )
        monitorId.meta['tip'] = "id of the monitor that will be used to do normalization"
        
        tofStart = inv.float(
            "tofStart", default = 0, validator = inv.greaterEqual( 0))
        tofStart.meta['tip'] = "monitor tof start. unit: mu seconds"

        tofEnd = inv.float(
            "tofEnd", default = 0, validator = inv.greaterEqual( 0))
        tofEnd.meta['tip'] = "monitor tof end. unit: mu seconds"

        pass # end of Inventory
    

    def __init__(self, name = "NormalizerUsingMonitorData"):
        CompBase.__init__(self, name)
        return


    def determineNorm(self):
        run = self._getInput( 'run' )
        monitorId = self.monitorId
        start = self.tofStart
        end = self.tofEnd
        from reduction.histCompat.MonitorNormCalcor import calcor
        monData = run.getMonitorItof( monitorId )
        return calcor.calcNorm( monData, start, end )


    def _configure(self):
        CompBase._configure(self)
        si = self.inventory
        self.monitorId = si.monitorId
        self.tofStart = si.tofStart
        self.tofEnd = si.tofEnd
        return
    

    pass # end of class NormalizerComp
    

# version
__id__ = "$Id: NormalizerUsingMonitorData.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
