#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from FacilityFrontEnd import FacilityFrontEnd

class TimeIndependentBackgroundRemover(FacilityFrontEnd):

    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Remove time-independent-background'
    pass

removeTIBG = TimeIndependentBackgroundRemover()


from reduction.core.TimeIndependentBackgroundRemover import TimeIndependentBackgroundRemover
removeTIBG.registerEngineFactory( 'per detector', TimeIndependentBackgroundRemover )


from reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as TIBGR_AOAD
removeTIBG.registerEngineFactory( 'average all detectors', TIBGR_AOAD)


removeTIBG.select( 'average all detectors')


__all__ = [ 'TimeIndependentBackgroundRemover', 'removeTIBG' ]


# version
__id__ = "$Id$"

# End of file 
