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

class NormalizationConstantFromIntegratedModeratorCurrent(base):

    def __init__(self):
        '''NormalizationConstantFromIntegratedModeratorCurrent()

        calculator that obtains normalization constant from integrated moderator current
        '''
        return

    def __call__(self, run):
        ic = run.getIntegratedCurrent()[0]
        return ic, 0.0        


# version
__id__ = "$Id$"

# End of file 
