#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.MaskFromVanadiumData
## Algorithms to calculate mask from vanadium calibration data
##


def findBadDetectors( Idet, minRatio=0.25, maxRatio=4. ):
    '''findBadDetectors( Idet, minRatio=0.25, maxRatio=4. ) -> bad detectors

    This algorithm is naive. It computes the average counts
    of all detectors, and then find those detectors that have
    excessive counts or nearly no counts, and return detector IDs
    of those detectors as bad detectors.
    
    Idet: I(det) of vandium data
    minRatio, maxRatio: bounds of ratio of intensity/(average_intensity)
    '''
    
    detIDs = Idet.axisFromName('detectorID').binCenters()
    
    ave_counts = Idet.sum()[0]/Idet.size()

    min = minRatio * ave_counts
    max = maxRatio * ave_counts

    ret = []
    
    for detID in detIDs:
        cnts = Idet[ detID ][0]
        if cnts < min: ret.append( detID )
        if cnts > max: ret.append( detID )
        continue

    return ret


# version
__id__ = "$Id$"

# End of file 
