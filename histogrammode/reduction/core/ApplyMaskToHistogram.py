#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



## \package reduction.core.ApplyMaskToHistogram
##
## Provides a reduction preprocessor that applies
## a detector mask to a histogram.
##




def applyMask( mask, histogram ):
    """applyMask( mask, histogram ) --> apply the given mask to the given histogram

    mask: detector mask. instance of instrument.DetectorMask
    histogram: I(det, pix, *) histogram on which the mask will be applied
    """
    global applyer
    applyer( mask, histogram )
    return


from instrument.DetectorMask import ApplyMask


class ApplyMaskToHistogram(ApplyMask):

    '''Apply mask to histogram

    Clear intensities of the given histogram at detectors and pixels
    that are in the mask.
    '''

    def apply(self, mask, histogram):
        '''apply( mask, histogram ): apply mask to histogram

        Set intensity at detectors and pixels in the mask to zero.
        '''
        detectorIDaxisName = 'detectorID'
        pixelIDaxisName = 'pixelID'
        
        for detID in histogram.axisFromName(detectorIDaxisName).binCenters():
            if mask.include( detID):
                histogram[ {detectorIDaxisName: detID} ].clear()
                continue
            continue
        
        for pxlID in histogram.axisFromName(pixelIDaxisName).binCenters():
            if mask.include( pixelID = pxlID ):
                histogram[ {pixelIDaxisName: pxlID} ].clear()
                continue
            continue

        for detID in histogram.axisFromName(detectorIDaxisName).binCenters():
            for pxlID in histogram.axisFromName(pixelIDaxisName).binCenters():
                if mask.include( detID, pxlID ):
                    subhist = histogram[
                        {detectorIDaxisName: detID, pixelIDaxisName: pxlID} ]
                    if isHistogram( subhist ): subhist.clear()
                    else: histogram[ {detectorIDaxisName: detID,
                                      pixelIDaxisName: pxlID} ] = 0,0
                    pass
                continue
            continue

        return


    pass # end of ApplyMaskToHistogram


applyer = ApplyMaskToHistogram()


def isHistogram(candidate):
    from histogram.Histogram import Histogram
    return isinstance( candidate, Histogram )


# version
__id__ = "$Id: MaxIncidentEnergySolver.odb 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
