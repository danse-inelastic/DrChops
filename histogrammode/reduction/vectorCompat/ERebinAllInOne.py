#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat.ERebinAllInOne
## rebin data in tof bins to energy bins

from TemplateCObject import TemplateCObject as Base
import reduction.reduction as red

import journal
debug = journal.debug('vectorCompat.ERebinAllInOne')


class ERebinAllInOne( Base):

    """energy rebinner
    
    rebin data in tof bins to energy bins
    """

    def count( self):
        """Number of times EBinCalc was called"""
        return self._count

    def __call__( self, pixelDistance, tBB, ebbNew, indata, outdata, inerrs,
                  outerrs):
        """rebinner( pixelDistance, tBB, ebbNew, indata, outdata, inerrs,
                  outerrs) -> None
        rebin some data, prorating counts from old bins to new ones based on
        overlap.
        Inputs:
            pixelDistance: distance from sample to pixel in mm
            tBB: StdVector holding time bin boundaries
            ebbNew: StdVector holding new energy bins
            inData: StdVector holding input data
            outData: StdVector into which rebinned data are placed.
            inerrs: StdVector holding input errors (squared, as always)
            outErrs: StdVector to hold output errors (squared, as always)
        Output:
            None
        Exceptions: ValueError, RuntimeError
        Notes: It is likely unwise to split off the error propagation in the
        normal course of things, as separate loops will run slower."""
        indata = indata.as( vectorType )
        inerrs = inerrs.as( vectorType )
        tBB = tBB.as( vectorType )
        eps = self._epsilon
        #if ( pixelDistance + eps < self._currdist) or \
        #      ( pixelDistance - eps > self._currdist):
        if abs(pixelDistance - self._currdist) > eps:
            self._ebincalc( pixelDistance, tBB, self._ebbo)
            self._currdist = pixelDistance
            self._count += 1
            debug.log( "old energy bin boundaries: %s" % (
                self._ebbo.asList(), ) )

        red.ERebinAllInOne_call( self._templateType, self._handle,
                                 self._ebbo._handle, ebbNew._handle,
                                 indata._handle, inerrs._handle,
                                 outdata._handle, outerrs._handle)
        return


    def __init__( self, datatype, numTBins, numEBins, ei, mod2SampleDist, 
                  dt, de, doKPOK=False, epsilon = 0.05):
        """ERebinAllInOne(datatype, numTBins, numEBins, ei, mod2SampleDist, 
                  dt, de, doKPOK=False, epsilon = 0.05) -> new rebinner
        Create a new rebinner.
        Inputs:
            datatype: type code--5: float, 6: double
            numTBins: how many time bins
            numEBins: how many (new) energy bins
            e_i: incident energy in meV
            mod2SampleDist: distance from moderator to sample in mm
            dt: time interval, in microseconds
            de: energy interval, in meV
            doKPOK: whether to apply (broken) k-prime over k correction
            epsilon: distance tolerance: if the last pixel had pixel-sample
                distance less than epsilon fdifferent from this sample, will
                reuse energy bins from that sample.
        Outputs:
            new rebinner instance
        Exceptions: ValueError
        Notes: (1) The bit about epsilon could be broken, as it was designed
        when the rebinner only new about 1 time bin boundaries array.
        (2) The k'/k correction is BROKEN and DEPRECATED. You should probably
        not use it. Also, this is probably an inefficient place to do it.
        (3) e_i is needed for both the k'/k correction, which you
        shouldn't do because it's BROKEN and DEPRECATED, and the EBinCalcor."""
        
        from reduction.vectorCompat.EBinCalcor import EBinCalcor

        self._ebincalc = EBinCalcor( datatype, ei, mod2SampleDist)
        self._count = 0
        self._epsilon = epsilon
        self._currdist = 0.0

        import stdVector
        self._ebbo = stdVector.vector( datatype, numTBins + 1, 0.0)

        import reduction.reduction as red
##         handle = red.ERebinAllInOne_ctor( datatype, numTBins, numEBins,
##                                           dt/de, doKPOK, ei)
        handle = red.ERebinAllInOne_ctor( datatype, numTBins, numEBins,
                                          1.0, doKPOK, ei)
        Base.__init__( self, datatype, handle, "ERebinAllInOne")

        debug.log("created rebinner: datatype = %s, ei = %s, mod2SampleDist = %s, numTBins = %s, numEBins = %s, dt/de=%s, doKPOK = %s" % (datatype, ei, mod2SampleDist, numTBins, numEBins, dt/de, doKPOK) )
        return


Rebinner = ERebinAllInOne


vectorType = "StdVectorNdArray"

# version
__id__ = "$Id: ERebinAllInOne.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
