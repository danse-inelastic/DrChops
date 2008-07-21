#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def normalize_iqqqe( IQQQE, ei, pixelPositions, pixel_area = 0.025*1./128):
    from histogram import histogram
    sa = histogram( 'solid_angle', IQQQE.axes() )
    calcSolidAngleQQQE( sa, ei, pixel_area, pixelPositions )

    #get numpy arrays
    I = IQQQE.I
    saarr = sa.I

    #find those cells where there should not be any counts
    zeros = saarr == 0
    #set those cells' counts to zero
    I[zeros] = 0
    #set zeros in solid angle matrix to 1, so that we won't have NaN
    saarr[zeros] = 1
    
    #normalize
    IQQQE /= sa
    return IQQQE


def calcSolidAngleQQQE( sa, ei, pixel_area, pixelPositions, mask_functor = None):
    '''calculate solid_angle(Qx,Qy,Qz,E)

    ei: incident energy
    pixelpositions: pixel positions numpy array (npixels, 3)
    mask_functor:
    '''
    #mask_functor has not been implemented yet

    axes = sa.axisNameList()
    assert len(axes) == 4
    assert axes[0] == 'Qx'
    assert axes[1] == 'Qy'
    assert axes[2] == 'Qz'
    assert axes[3] == 'energy'

    qxaxis = sa.axisFromName( 'Qx' )
    qxbbs = qxaxis.binBoundaries().asNumarray()
    qxbegin, qxend, qxstep = qxbbs[0], qxbbs[-1], qxbbs[1]-qxbbs[0]

    qyaxis = sa.axisFromName( 'Qy' )
    qybbs = qyaxis.binBoundaries().asNumarray()
    qybegin, qyend, qystep = qybbs[0], qybbs[-1], qybbs[1]-qybbs[0]

    qzaxis = sa.axisFromName( 'Qz' )
    qzbbs = qzaxis.binBoundaries().asNumarray()
    qzbegin, qzend, qzstep = qzbbs[0], qzbbs[-1], qzbbs[1]-qzbbs[0]
    
    eaxis = sa.axisFromName( 'energy' )
    ebbs = eaxis.binBoundaries().asNumarray()
    ebegin, eend, estep = ebbs[0], ebbs[-1], ebbs[1]-ebbs[0]
    
    npixels = len(pixelPositions)
    from numpyext import getdataptr
    pixelPositions = getdataptr( pixelPositions )
    
    from arcseventdata import calcSolidAngleQQQE_numpyarray

    return calcSolidAngleQQQE_numpyarray( 
        qxbegin, qxend, qxstep,
        qybegin, qyend, qystep,
        qzbegin, qzend, qzstep,
        ebegin, eend, estep,
        sa.data().storage().asNumarray(),
        ei,
        pixel_area,
        npixels, pixelPositions)


# version
__id__ = "$Id$"

#  End of file 
