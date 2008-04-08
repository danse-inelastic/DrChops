#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.histCompat.MonitorNormalizer
## normalize datasets using monitor counts
##
## this is a wrapper of reduction.vectorCompat.MonitorNormalizer


from stdVector import vector

class MonitorNormalizer( object):


    def determineNorm( self, monitorHist, start, end):
        """determineNorm( monitorData, start, end) -> None
        Determine the normalization factor from a given monitor data set by
        integrating over the range from start to but not including end with
        bin size dt.
        Inputs:
            monitorData: monitor histogram
            start, end: channel range over which to integrate
            dt: bin size (float)
        Output:
            None (result stored in this object for later use.
        Exceptions: ValueError, IndexError
        Notes: raises ValueError if norm is equal to 0.0. Other exceptions
        raised in monitorData.integrate"""
        
        # determine dt
        tofList = monitorHist.tof().storage().asList()
        dt = tofList[1] - tofList[0]

        monData = monitorHist.data().storage()
        self._normalizer.determineNorm( monData, start, end, dt)

        return


    def normalize( self, inputHist, outputHist):
        """normalize( inputHist, outputHist) -> outputHist
        Multiply each element of dataset by 1.0/norm, propagate errors.
        Inputs:
            inputHist: histogram instance
            outputHist: histogram instance 
        Output: outputHist
        Exceptions: ValueError, TypeError
        Notes:
            (1) In order to change histogram in place, pass histogram in
            both the inputHist and outputHist slots.
            (2) This object allocates and maintains a temporary vector for
            vectorCompat monitorNormalizer to use; it reallocates only when
            the size of the histogram being normalized changes.."""

        indata = inputHist.data().storage()
        inerrs = inputHist.errors().storage()
        outdata = outputHist.data().storage()
        outerrs = outputHist.errors().storage()

        if not self._tempVector:
            self._tempVector = vector( indata.datatype(), indata.size())
        else:
            if self._tempVector.size() != indata.size():
                self._tempVector = vector( indata.datatype(), indata.size())

        # need to zero out tempVector? Apparently not, but still...
        self._normalizer.normalize( indata, outdata, inerrs, outerrs,
                                    self._tempVector)
        
        return outputHist


    def norm( self):
        """norm() -> present value of norm"""
        return self._normalizer._norm


    def sigma_norm2( self):
        """sigma_norm2() -> square error of present value of norm"""
        return self._normalizer._sigma2
        

    def __init__( self, errorProp = None):

        from reduction.vectorCompat.MonitorNormalizer import MonitorNormalizer
        self._normalizer = MonitorNormalizer()

        self._tempVector = None

        return

    
# version
__id__ = "$Id: MonitorNormalizer.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
