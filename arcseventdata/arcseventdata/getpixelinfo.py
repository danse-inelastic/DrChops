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


def getpixelinfo(
    positions, 
    npacks = 115, ndetsperpack = 8, npixelsperdet = 128):
    
    '''convert pixel positions to angles of pixels
    
    positions: an array of positions (3*ntotpixels floats)
    npacks: # of packs
    ndetsperpack: # of detectors per pack
    npixelsperdet: # of pixels per detector
    return: histograms phi(pixel) and psi(pixel)
    '''

    from numpy import sqrt, sum, arccos, arctan2, fromstring, array, pi
    
    ntotpxls = (npacks+1)*ndetsperpack*npixelsperdet 
    positions.shape = ntotpxls, 3

    import histogram
    phi_p = histogram.histogram(
        'phi_pdp',
        [
        ('detectorpackID', range(npacks+1)),
        ('detectorID', range(ndetsperpack) ),
        ('pixelID', range(npixelsperdet) ),
        ] )
    
    psi_p = histogram.histogram(
        'psi_pdp',
        [
        ('detectorpackID', range(npacks+1)),
        ('detectorID', range(ndetsperpack) ),
        ('pixelID', range(npixelsperdet) ),
        ] )

    dist_p = histogram.histogram(
        'dist_pdp',
        [
        ('detectorpackID', range(npacks+1)),
        ('detectorID', range(ndetsperpack) ),
        ('pixelID', range(npixelsperdet) ),
        ] )

    phi_arr = array( phi_p.data().storage().asNumarray(), copy = 0 )
    phi_arr.shape = -1, 
    psi_arr = array( psi_p.data().storage().asNumarray(), copy = 0 )
    psi_arr.shape = -1,
    dist_arr = array( dist_p.data().storage().asNumarray(), copy = 0 )
    dist_arr.shape = -1,

    for i in range(ntotpxls):
        x,y,z = r = positions[i]
        #phi is the angle between the scattered neutron and the incident beam
        # note: assuming we use "Instrument scientist" coord system
        # z: up (opposite of gravity)
        # x: neutron beam downstream
        sample2pixel = sqrt(sum(r*r))
        phi = arccos( x / sample2pixel )
        psi = arctan2( z, y )

        phi_arr[i] = phi
        psi_arr[i] = psi
        dist_arr[i] = sample2pixel
        continue

    phi_arr *= 180/pi
    psi_arr *= 180/pi
    
    return phi_p, psi_p, dist_p

# version
__id__ = "$Id$"

#  End of file 
