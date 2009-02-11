#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2009  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def normalize_ihkle( IHKLE, ei, ub, pixelPositions, pixel_area = 0.025*1./128):
    from histogram import histogram
    sa = histogram( 'solid_angle', IHKLE.axes() )
    calcSolidAngleHKLE( sa, ei, ub, pixel_area, pixelPositions )

    #get numpy arrays
    I = IHKLE.I
    saarr = sa.I

    #find those cells where there should not be any counts
    zeros = saarr == 0
    #set those cells' counts to zero
    I[zeros] = 0
    #set zeros in solid angle matrix to 1, so that we won't have NaN
    saarr[zeros] = 1
    
    #normalize
    IHKLE /= sa
    return IHKLE


def calcSolidAngleHKLE( sa, ei, ub, pixel_area, pixelPositions, mask_functor = None):
    '''calculate solid_angle(h,k,l,E)

    ei: incident energy
    pixelpositions: pixel positions numpy array (npixels, 3)
    mask_functor:
    '''
    #mask_functor has not been implemented yet

    axes = sa.axisNameList()
    assert len(axes) == 4
    assert axes[0] == 'h'
    assert axes[1] == 'k'
    assert axes[2] == 'l'
    assert axes[3] == 'energy'

    haxis = sa.axisFromName( 'h' )
    hbbs = haxis.binBoundaries().asNumarray()
    hbegin, hend, hstep = hbbs[0], hbbs[-1], hbbs[1]-hbbs[0]

    kaxis = sa.axisFromName( 'k' )
    kbbs = kaxis.binBoundaries().asNumarray()
    kbegin, kend, kstep = kbbs[0], kbbs[-1], kbbs[1]-kbbs[0]

    laxis = sa.axisFromName( 'l' )
    lbbs = laxis.binBoundaries().asNumarray()
    lbegin, lend, lstep = lbbs[0], lbbs[-1], lbbs[1]-lbbs[0]
    
    eaxis = sa.axisFromName( 'energy' )
    ebbs = eaxis.binBoundaries().asNumarray()
    ebegin, eend, estep = ebbs[0], ebbs[-1], ebbs[1]-ebbs[0]
    
    npixels = len(pixelPositions)
    from numpyext import getdataptr
    pixelPositions = getdataptr( pixelPositions )
    
    from arcseventdata import calcSolidAngleHKLE_numpyarray

    return calcSolidAngleHKLE_numpyarray( 
        hbegin, hend, hstep,
        kbegin, kend, kstep,
        lbegin, lend, lstep,
        ebegin, eend, estep,
        sa.data().storage().asNumarray(),
        ei, ub,
        pixel_area,
        npixels, pixelPositions)


# version
__id__ = "$Id$"

#  End of file 
