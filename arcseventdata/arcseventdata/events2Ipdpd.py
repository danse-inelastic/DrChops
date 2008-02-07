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


def events2Ipdpd(events, n, Ipdpd, pixelpositions,
                 npacks = 115, ndetsperpack = 8, npixelsperdet = 128,
                 tofUnit = 1.e-7, mod2sample = 13.5,
                 emission_time = 0.0):
    axes = Ipdpd.axes()
    assert len(axes) == 4
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]

    assert axes[3].name() == 'd spacing'
    d_axis = axes[3]
    d_boundaries = d_axis.binBoundaries().asNumarray()
    d_begin = d_boundaries[0]
    d_step = d_boundaries[1] - d_boundaries[0]
    d_end = d_boundaries[-1]

    assert npacks == axes[0].size()
    assert ndetsperpack == axes[1].size()
    assert npixelsperdet == axes[2].size()
    ntotpixels = (npacks)*ndetsperpack*npixelsperdet
    
    import arcseventdata as binding
    return binding.events2Ipixd_numpyarray(
        events, n,
        0, ntotpixels, 1,
        d_begin, d_end, d_step,
        Ipdpd.data().storage().asNumarray(),
        pixelpositions, ntotpixels, tofUnit, mod2sample,
        emission_time)


# version
__id__ = "$Id$"

#  End of file 
