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


## \package reduction.pyre.TimeIndependentBackgroundRemover_AverageOverAllDetectors
## remove tof-independent background from data
##
## This is different from reduction.pyre.TimeIndependentBackgroundRemover_PerDetector in that it calculates
## background by averaging over all detectors
##


from TimeIndependentBackgroundRemover_PerDetector import TimeIndependentBackgroundRemover_PerDetector as base


class TimeIndependentBackgroundRemover_AverageOverAllDetectors(base):

    
    from reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as Engine


    __doc__ = Engine.__doc__


    def __init__(self,
                 name = "TimeIndependentBackgroundRemover_AverageOverAllDetectors"
                 ):
        
        base.__init__(self, name)
        return


    pass # end of TimeIndependentBackgroundRemover_AverageOverAllDetectors


# version
__id__ = "$Id: TimeIndependentBackgroundRemover_AverageOverAllDetectors.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
