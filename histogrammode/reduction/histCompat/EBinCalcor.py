#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.histCompat.EBinCalcor
## calculate energy bins out of tof bins. This is really not used by anyone.
## It is a wrapper of reduction.vectorCompat.EBinCalcor

class EBinCalcor( object):

    """energy bin calculator

    calculate energy bins out of tof bins
    """


    def __call__(self, pixelDist, timeHistogram, energyHistogram):
        """ebincalcor( pixelDist, tBinBoundsVec, eBinBoundsVec) -> None
        Calculate energy bin boundaries for histogram with energy axis given pixel
        distance and histogram with tof axis.
        inputs:
            pixelDist: distance from sample to pixel (float)
            timeHistogram (instance of Histogram with axis "tof")
            energyHistogram (instance of Histogram with axis "Energy")
        outputs:
            None (results stored in energy axis of energyHistogram)
        Exceptions: ValueError, RuntimeError"""
        tofAxis = timeHistogram.axisFromName( "tof")
        tofVector = tofAxis.storage()

        energyAxis = energyHistogram.axisFromName( "energy")
        energyVector = energyAxis.storage()
        
        self._calcor( pixelDist, tofVector, energyVector)
        return
    

    def __init__(self, datatype, ei, mod2samp):
        """EBinCalcor( datatype, e_i, mod2sampDist) -> new instance
        Create new instance to compute energy bin bounds given time bn bounds.
        Inputs:
            datatype: type code (int)
            e_i: incident energy in meV (float)
            mod2sampDist: distance from moderator to sample in mm (float)
        Output:
            new instance
        Exceptions: ValueError
        Notes: (1) ValueError raised if inappropriate type code. Recognized
        types are:
            5........float
            6........double
        (2) Handle kept as TWrapper."""

        from reduction.vectorCompat.EBinCalcor import EBinCalcor
        self._calcor = EBinCalcor( datatype, ei, mod2samp)

        return


# version
__id__ = "$Id: EBinCalcor.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
