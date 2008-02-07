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


def events2Itof(
    events, n, ntotpixels,
    Itof,
    tofUnit = 1.e-7):
    
    axes = Itof.axes()
    assert len(axes) == 1
    assert axes[0].name() == 'tof'
    
    tof_axis = axes[0]
    import units
    unit = tof_axis.unit()/units.time.second
    
    tof_boundaries = tof_axis.binBoundaries().asNumarray()
    tof_begin = tof_boundaries[0] * unit
    tof_step = (tof_boundaries[1] - tof_boundaries[0]) * unit
    tof_end = tof_boundaries[-1] * unit

    import arcseventdata as binding
    return binding.events2Itof_numpyarray(
        events, n,
        tof_begin, tof_end, tof_step,
        Itof.data().storage().asNumarray(),
        ntotpixels, tofUnit,
        )


# version
__id__ = "$Id$"

#  End of file 
