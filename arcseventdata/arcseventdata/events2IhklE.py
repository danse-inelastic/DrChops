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


def events2IhklE(
    events, n, IhklE, Ei, ub, pixelpositions,
    tofUnit = 1.e-7, mod2sample = 13.5,
    emission_time = 0.0):

    intensity_npy_typecode = _histtype_to_npytypecode( IhklE.typeCode() )
    
    axes = IhklE.axes()
    assert len(axes) == 4
    
    assert axes[0].name() == 'h'
    h_axis = axes[0]
    h_boundaries = h_axis.binBoundaries().asNumarray()
    h_begin = h_boundaries[0]
    h_step = h_boundaries[1] - h_boundaries[0]
    h_end = h_boundaries[-1] + h_step/100.

    assert axes[1].name() == 'k'
    k_axis = axes[1]
    k_boundaries = k_axis.binBoundaries().asNumarray()
    k_begin = k_boundaries[0]
    k_step = k_boundaries[1] - k_boundaries[0]
    k_end = k_boundaries[-1] + k_step/100.
 
    assert axes[2].name() == 'l'
    l_axis = axes[2]
    l_boundaries = l_axis.binBoundaries().asNumarray()
    l_begin = l_boundaries[0]
    l_step = l_boundaries[1] - l_boundaries[0]
    l_end = l_boundaries[-1] + l_step/100.

    assert axes[3].name() == 'energy'
    E_axis = axes[3]
    E_boundaries = E_axis.binBoundaries().asNumarray()
    E_begin = E_boundaries[0]
    E_step = E_boundaries[1] - E_boundaries[0]
    E_end = E_boundaries[-1]

    ntotpixels = len(pixelpositions)
    
    from numpyext import getdataptr
    pixelpositions_ptr = getdataptr( pixelpositions )
    
    import arcseventdata as binding
    binding.events2IhklE_numpyarray(
        events, n,
        h_begin, h_end, h_step,
        k_begin, k_end, k_step,
        l_begin, l_end, l_step,
        E_begin, E_end, E_step,
        IhklE.data().storage().asNumarray(),
        Ei, ub,
        pixelpositions_ptr, ntotpixels, tofUnit, mod2sample,
        emission_time, intensity_npy_typecode)

    return IhklE



def _histtype_to_npytypecode( type ):
    # the following implementation does not work because of difference
    # of handling in hdf5 type codes and numpy type codes
    # we should all use numpy type codes and not hdf5 codes
    #from array_kluge.create_type_lookup_table import gettypename
    #name = gettypename( type )

    name = {
        24: 'int32',
        6: 'float64',
        } [ type ]
    
    import numpy
    return numpy.dtype( name ).num


# version
__id__ = "$Id$"

#  End of file 
