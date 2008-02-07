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


def events2IpdpE(events, n, IpdpE, Ei, pixelpositions,
                 npacks = 115, ndetsperpack = 8, npixelsperdet = 128,
                 tofUnit = 1.e-7, mod2sample = 13.5,
                 emission_time = 0.0):
    axes = IpdpE.axes()
    assert len(axes) == 4
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]

    assert axes[3].name() == 'energy'
    E_axis = axes[3]
    E_boundaries = E_axis.binBoundaries().asNumarray()
    E_begin = E_boundaries[0]
    E_step = E_boundaries[1] - E_boundaries[0]
    E_end = E_boundaries[-1]

    assert npacks == axes[0].size()-1
    assert ndetsperpack == axes[1].size()
    assert npixelsperdet == axes[2].size()
    ntotpixels = (npacks+1)*ndetsperpack*npixelsperdet
    
    import arcseventdata as binding
    return binding.events2IpixE_numpyarray(
        events, n,
        0, ntotpixels, 1,
        E_begin, E_end, E_step,
        IpdpE.data().storage().asNumarray(),
        Ei,
        pixelpositions, ntotpixels, tofUnit, mod2sample,
        emission_time)


# version
__id__ = "$Id$"

#  End of file 
