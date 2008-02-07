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


def events2Ipdpt(events, n, Ipdpt, 
                 tofUnit = 1.e-7):
    axes = Ipdpt.axes()
    assert len(axes) == 4
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]

    assert axes[3].name() == 'tof'
    tof_axis = axes[3]
    tof_boundaries = tof_axis.binBoundaries().asNumarray()
    tof_begin = tof_boundaries[0]
    tof_step = tof_boundaries[1] - tof_boundaries[0]
    tof_end = tof_boundaries[-1]

    ntotpixels = Ipdpt.size() / tof_axis.size()
    
    import arcseventdata as binding
    return binding.events2Ipixtof_numpyarray(
        events, n,
        0, ntotpixels, 1,
        tof_begin, tof_end, tof_step,
        Ipdpt.data().storage().asNumarray(),
        ntotpixels, tofUnit)


# version
__id__ = "$Id$"

#  End of file 
