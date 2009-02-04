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


def events2IpdpEi(events, n, IpdpEi, pixelpositions,
                 tofUnit = 1.e-7, mod2sample = 13.5,
                 emission_time = 0.0):
    axes = IpdpEi.axes()
    assert len(axes) == 4
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]

    assert axes[3].name() == 'Ei'
    Ei_axis = axes[3]
    Ei_boundaries = Ei_axis.binBoundaries().asNumarray()
    Ei_begin = Ei_boundaries[0]
    Ei_step = Ei_boundaries[1] - Ei_boundaries[0]
    Ei_end = Ei_boundaries[-1]

    ntotpixels = len( pixelpositions )
    from numpyext import getdataptr
    pixelpositions = getdataptr( pixelpositions )
    
    import arcseventdata as binding
    return binding.events2IpixEi_numpyarray(
        events, n,
        0, ntotpixels, 1,
        Ei_begin, Ei_end, Ei_step,
        IpdpEi.data().storage().asNumarray(),
        pixelpositions, ntotpixels, tofUnit, mod2sample,
        emission_time)


# version
__id__ = "$Id$"

#  End of file 
