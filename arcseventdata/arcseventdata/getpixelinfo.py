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


## obtain histograms about pixel h(pack, tube, pixel)
##   - phi. scattering angle
##   - psi. azimuthal angle
##   - dist. distance from sample to pixel.


def getpixelinfo(
    positions, detaxes):
    
    '''convert pixel positions to angles of pixels
    
    positions: an array of positions (3*ntotpixels floats)
    npacks: # of packs
    ndetsperpack: # of detectors per pack
    npixelsperdet: # of pixels per detector
    return: histograms phi(pixel) and psi(pixel)
    '''

    from numpy import sqrt, sum, arccos, arctan2, fromstring, array, pi

    positions.shape = -1, 3

    import histogram
    phi_p = histogram.histogram(
        'phi_pdp', detaxes )
    
    psi_p = histogram.histogram(
        'psi_pdp', detaxes )

    dist_p = histogram.histogram(
        'dist_pdp', detaxes )

    phi_arr = array( phi_p.data().storage().asNumarray(), copy = 0 )
    phi_arr.shape = -1, 
    psi_arr = array( psi_p.data().storage().asNumarray(), copy = 0 )
    psi_arr.shape = -1,
    dist_arr = array( dist_p.data().storage().asNumarray(), copy = 0 )
    dist_arr.shape = -1,

    ntotpxls = len( positions )
    
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
