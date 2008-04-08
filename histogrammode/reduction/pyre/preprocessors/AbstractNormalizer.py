#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.pyre.AbstractNormalizer
## provides base class for dataset normalizers
## subclass of AbstractNormalizerComp only needs to implement method 'determineNorm'

from Connectable import Connectable as base

class AbstractNormalizer(base):

    "base class for normalizer pyre component"


    def __init__(self, name, facility="Normalizer"):
        base.__init__(self, name, facility )
        return
    

    def norm(self):
        return self._norm


    def determineNorm(self):
        "return norm, norm_err2"
        raise NotImplementedError
    

    sockets = {
        'in': ['run', 'histogram'],
        'out': ['histogram'],
        }


    def _update(self):
        """normalize histotgram
        """
        histogram = self._getInput( 'histogram' )
        self._norm = norm = self.determineNorm()
        histogram /= norm
        self._setOutput( 'histogram', histogram )
        return




# version
__id__ = "$Id: AbstractNormalizer.py 1434 2007-11-05 16:02:32Z linjiao $"

# End of file 
