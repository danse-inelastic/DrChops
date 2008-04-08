#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def maskMatrix( mask, axes ):
    '''Create a nD array that contains 1s and 0s.
    Each element in the array corresponds to a pixel.
    An element is 1 means that pixel is masked (vetoed),
    and an element is 0 means that pixel is not masked.

    This function creates such a nD array from an instance of instrument.DetectorMask.
    A list of detector-related axes is also needed as an input.
    '''

    from histogram import histogram
    mask_dp = histogram( 'mask', axes, data_type = 'int')

    if mask is None: return mask_dp

    detaxis = mask_dp.axisFromName( 'detectorID' )
    pixaxis = mask_dp.axisFromName( 'pixelID' )
                                      
    dets = detaxis.binCenters()
    pixs = pixaxis.binCenters()
        
    from numpy import ones, zeros
    for det in mask.excludedDetectors:
        if det not in dets: continue
        mask_dp [ {'detectorID':det} ] = 1, 0
        continue
    for pix in mask.excludedPixels:
        if pix not in pixs: continue
        mask_dp [ {'pixelID':pix} ] = 1, 0
        continue
    for det,pix in mask.excludedSingles:
        if det not in dets: continue
        if pix not in pixs: continue
        mask_dp [ {'detectorID':det, 'pixelID':pix} ] = 1, 0
        continue
    
    return mask_dp


def test():
    from instrument import mask
    m = mask()
    from histogram import axis
    detaxis = axis( 'detectorID', range(10) )
    pixaxis = axis( 'pixelID', range(10) )
    m = maskMatrix( m, (detaxis, pixaxis) )
    return


if __name__ == '__main__' : test()

# version
__id__ = "$Id$"

# End of file 

