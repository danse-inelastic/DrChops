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


def events2IQE(events, n, IQE, Ei, pixelpositions,
               tofUnit = 1.e-7, mod2sample = 13.5,
               emission_time = 0.0):
    axes = IQE.axes()
    assert len(axes) == 2
    
    assert axes[0].name() == 'Q'
    Q_axis = axes[0]
    Q_boundaries = Q_axis.binBoundaries().asNumarray()
    Q_begin = Q_boundaries[0]
    Q_step = Q_boundaries[1] - Q_boundaries[0]
    Q_end = Q_boundaries[-1] + Q_step/10.

    assert axes[1].name() == 'energy'
    E_axis = axes[1]
    E_boundaries = E_axis.binBoundaries().asNumarray()
    E_begin = E_boundaries[0]
    E_step = E_boundaries[1] - E_boundaries[0]
    E_end = E_boundaries[-1] + E_step/10.

    ntotpixels = len(pixelpositions)
    
    from numpyext import getdataptr
    pixelpositions_ptr = getdataptr( pixelpositions )
    
    import arcseventdata as binding
    binding.events2IQE_numpyarray(
        events, n,
        Q_begin, Q_end, Q_step,
        E_begin, E_end, E_step,
        IQE.data().storage().asNumarray(),
        Ei,
        pixelpositions_ptr, ntotpixels, tofUnit, mod2sample,
        emission_time)

    return IQE


# version
__id__ = "$Id$"

#  End of file 
