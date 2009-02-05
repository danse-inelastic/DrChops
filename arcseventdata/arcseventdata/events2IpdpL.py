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


def events2IpdpL(events, n, IpdpL, pixelpositions,
                 tofUnit = 1.e-7, mod2sample = 13.5,
                 emission_time = 0.0):
    axes = IpdpL.axes()
    assert len(axes) == 4
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]

    assert axes[3].name() == 'L'
    L_axis = axes[3]
    L_boundaries = L_axis.binBoundaries().asNumarray()
    L_begin = L_boundaries[0]
    L_step = L_boundaries[1] - L_boundaries[0]
    L_end = L_boundaries[-1]

    ntotpixels = len( pixelpositions )
    from numpyext import getdataptr
    pixelpositions = getdataptr( pixelpositions )
    
    import arcseventdata as binding
    return binding.events2IpixL_numpyarray(
        events, n,
        0, ntotpixels, 1,
        L_begin, L_end, L_step,
        IpdpL.data().storage().asNumarray(),
        pixelpositions, ntotpixels, tofUnit, mod2sample,
        emission_time)


# version
__id__ = "$Id$"

#  End of file 
