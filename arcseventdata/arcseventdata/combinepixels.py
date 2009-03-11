#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                        (C) 2007-2009  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def combinepixels(ARCSxml, detaxes, pixel_resolution):
    # data for resolution=1

    # positions
    from _getinstrumentinfo import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    positions = infos['pixelID-position mapping array']
    detaxes0 = infos['detector axes']
    npacks, ndetsperpack, npixelsperdet = [axis.size() for axis in detaxes0]
    positions.shape = npacks, ndetsperpack, npixelsperdet, 3

    # radii and heights
    from instrument.nixml import parse_file
    instrument = parse_file( ARCSxml )
    from getpixelsizes import getpixelsizes
    radii, heights = getpixelsizes(
        instrument, npacks, ndetsperpack, npixelsperdet)

    #
    dists, phis, psis, solidangles, dphis, dpsis = \
           calcpixelinfo(positions, radii, heights, pixel_resolution)

    import histogram
    # scattering angles
    phi_p = histogram.histogram('phi_pdp', detaxes )
    phi_p.I[:] = phis
    
    psi_p = histogram.histogram('psi_pdp', detaxes )
    psi_p.I[:] = psis
    
    # distances
    dist_p = histogram.histogram('dist_pdp', detaxes )
    dist_p.I[:] = dists

    # quantities related to the sizes of pixels
    # solid angles
    solidangle_p = histogram.histogram('solidangle_pdp', detaxes)
    solidangle_p.I[:] = solidangles

    # dphi
    dphi_p = histogram.histogram('dphi_pdp', detaxes )
    dphi_p.I[:] = dphis

    # dpsi
    dpsi_p = histogram.histogram('dpsi_pdp', detaxes )
    dpsi_p.I[:] = dpsis
    
    return phi_p, psi_p, dist_p, solidangle_p, dphi_p, dpsi_p


def calcpixelinfo(
    positions, radii, heights, resolution):

    # make sure shapes are consistent
    npacks, ntubesperpack, npixelspertube = shape = radii.shape
    assert heights.shape == shape
    assert positions.shape == shape + (3,)

    #
    assert npixelspertube%resolution==0

    #
    tmpshape = npacks, ntubesperpack, npixelspertube/resolution, resolution

    positions.shape = tmpshape + (3,)
    newpositions = positions.sum(axis=-2)/resolution
    #restore shape
    positions.shape = shape + (3,)

    newshape = npacks, ntubesperpack, npixelspertube/resolution
    assert newpositions.shape == newshape + (3,)

    radii.shape = heights.shape = tmpshape
    newradii = radii[:,:,:,0]
    newheights = heights.sum(axis=-1)
    assert newradii.shape == newshape
    assert newheights.shape == newshape

    from getpixelinfo import calcpixelinfo
    return calcpixelinfo(newpositions, newradii, newheights)


import numpy as N

# version
__id__ = "$Id$"

#  End of file 
