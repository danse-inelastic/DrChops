#!/usr/bin/env python
# Jiao Lin (c) 2006 All rights reserved


## \package reduction.histCompat.Normalizer
## generic normalizer to normalize datasets 
##

from Normalizer import Normalizer


class HCNormalizer( object):

    """histogram collection normalizer

    In reduction, it is a common practise to normalize data by intensity
    of incident neutron beam. 
    """

    def normalize( self, histC):
        """normalize( histC ) --> histC
        normalize all histogram in histC
        """
        for hist in histC.getAll(): self._engine.normalize( hist )
        return histC


    def norm( self):
        """norm() -> (norm, norm_err2)"""
        return self._norm, self._sigma2


    def __init__( self, norm, sigma2):
        self._norm, self._sigma2 = norm, sigma2
        self._engine = Normalizer( norm, sigma2 )
        return
    


# version
__id__ = "$Id: Normalizer.py 568 2005-07-25 20:56:06Z tim $"

# End of file
