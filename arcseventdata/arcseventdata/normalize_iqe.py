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


def normalize_iqe( IQE, ei, pixelPositions, pixelSolidAngles):
    from histogram import histogram
    sa = histogram( 'solid_angle', IQE.axes() )
    calcSolidAngleQE( sa, ei, pixelPositions, pixelSolidAngles )

    #get numpy arrays
    I = IQE.I
    saarr = sa.I

    #find those cells where there should not be any counts
    zeros = saarr == 0
    #set those cells' counts to zero
    I[zeros] = 0
    #set zeros in solid angle matrix to 1, so that we won't have NaN
    saarr[zeros] = 1
    
    #normalize
    IQE /= sa
    return IQE


def calcSolidAngleQE( sa, ei, pixelPositions, pixelSolidAngles,
                      mask_functor = None):
    '''calculate solid_angle(Q,E)

    ei: incident energy
    qaxis: Q axis
    eaxis: energy axis
    pixelpositions: pixel positions numpy array (npixels, 3)
    mask_functor:
    '''
    #mask_functor has not been implemented yet

    axes = sa.axisNameList()
    assert len(axes) == 2
    assert axes[0] == 'Q'
    assert axes[1] == 'energy'

    qaxis = sa.axisFromName( 'Q' )
    qbbs = qaxis.binBoundaries().asNumarray()
    qbegin, qend, qstep = qbbs[0], qbbs[-1], qbbs[1]-qbbs[0]
    qend += qstep/10.
    
    eaxis = sa.axisFromName( 'energy' )
    ebbs = eaxis.binBoundaries().asNumarray()
    ebegin, eend, estep = ebbs[0], ebbs[-1], ebbs[1]-ebbs[0]
    eend += estep/10.
    
    npixels = len(pixelPositions)
    from numpyext import getdataptr
    pixelPositions = getdataptr( pixelPositions )
    pixelSolidAngles = getdataptr( pixelSolidAngles )
    
    from arcseventdata import calcSolidAngleQE_numpyarray

    return calcSolidAngleQE_numpyarray( 
        qbegin, qend, qstep, ebegin, eend, estep,
        sa.data().storage().asNumarray(),
        ei, npixels, pixelPositions, pixelSolidAngles)


# version
__id__ = "$Id$"

#  End of file 
