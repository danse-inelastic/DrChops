#!/usr/bin/env python
# Jiao Lin (c) 2006 All rights reserved


## \package reduction.histCompat.Normalizer
## generic normalizer to normalize datasets 
##


class Normalizer( object):


    def normalize( self, inputHist, outputHist = None):
        """normalize( inputHist, outputHist) -> outputHist
        Multiply each element of dataset by 1.0/norm, propagate errors.
        Inputs:
            inputHist: histogram instance
            outputHist: histogram instance 
        Output: outputHist
        Exceptions: ValueError, TypeError
        Notes:
            (1) In order to change histogram in place, omit the outputHist
        """
        if outputHist is None:
            inputHist/=(self._norm, self._sigma2)
            return inputHist
        outputHist = inputHist/(self._norm, self._sigma2)
        return outputHist


    def norm( self):
        """norm() -> (norm, norm_err2)"""
        return self._norm, self._sigma2


    def __init__( self, norm, sigma2):
        self._norm, self._sigma2 = norm, sigma2
        return

    
# version
__id__ = "$Id: Normalizer.py 568 2005-07-25 20:56:06Z tim $"

# End of file
