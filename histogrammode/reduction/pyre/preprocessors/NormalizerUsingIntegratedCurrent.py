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

## \package reduction.pyre.NormalizerUsingIntegratedCurrent
## normalizer using moderator integrated current


from AbstractNormalizer import AbstractNormalizer as base

class NormalizerUsingIntegratedCurrent(base):


    '''pyre component of normalizer.
    Uses integrated current of moderator to calculate normalization factor.
    '''

    def __init__(self, name = "NormalizerUsingIntegratedCurrent"):
        base.__init__(self, name)
        return


    def determineNorm(self):
        run = self._getInput('run')
        ic = run.getIntegratedCurrent()[0]
        return ic, 0.0


    pass # end of class NormalizerUsingIntegratedCurrent
    


# version
__id__ = "$Id: NormalizerUsingIntegratedCurrent.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
