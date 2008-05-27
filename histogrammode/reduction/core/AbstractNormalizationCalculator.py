#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



## \package reduction.core.NormalizationCalculator
## Calculate normalization constant for a "run"


class AbstractNormalizationCalculator:

    "abstract base class to deterimine normalization constant"

    def __call__(self, run):
        """calculate normalization constant for an experimental run

        @run: experiment run. instance of measurement.Run
        @return: normalization constant
        @rtype:  float
        """
        raise NotImplementedError , "%s must provide __call__()" % (
            self.__class__.__name__)


    pass #end of AbstractNormalizationCalculator


# version
__id__ = "$Id$"

# End of file 
