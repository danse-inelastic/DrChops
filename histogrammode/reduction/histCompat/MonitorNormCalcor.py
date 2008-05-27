#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from NormCalcor import NormCalcor


class MonitorNormCalcor( NormCalcor ):

    """ Uses integrated counts at monitor as norm
    """
    
    def calcNorm(self, monitorHist, tofStart, tofEnd ):
        tofaxis = monitorHist.axisFromName('tof')
        tofunit = tofaxis.unit()

        #tof bin centers
        t = tofaxis.binCenters()

        from reduction.units import isDimensional
        if isDimensional( tofStart ): tofStart /= tofunit
        if isDimensional( tofEnd ): tofEnd /= tofunit
        
        if tofStart > tofEnd:
            raise ValueError , "tofStart(%s) > tofEnd(%s)" %(
                tofStart, tofEnd)
        
        if abs(tofStart) < 1e-10 and abs(tofEnd) < 1e-10:
            tofStart = t[0]; tofEnd = t[-1]
            pass
        if tofStart < t[0]: tofStart = t[0]
        if tofEnd > t[-1]: tofEnd = t[-1]
        
        subhist = monitorHist[ (tofStart, tofEnd) ]
        n, nerr2 = subhist.sum()
        return n, nerr2


    pass # end of MonitorNormCalcor


calcor = MonitorNormCalcor()


# version
__id__ = "$Id$"

# End of file
