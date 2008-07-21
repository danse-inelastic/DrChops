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


def events2IQQQE(
    events, n, IQQQE, Ei, pixelpositions,
    tofUnit = 1.e-7, mod2sample = 13.5,
    emission_time = 0.0):

    intensity_npy_typecode = _histtype_to_npytypecode( IQQQE.typeCode() )
    
    axes = IQQQE.axes()
    assert len(axes) == 4
    
    assert axes[0].name() == 'Qx'
    Qx_axis = axes[0]
    Qx_boundaries = Qx_axis.binBoundaries().asNumarray()
    Qx_begin = Qx_boundaries[0]
    Qx_step = Qx_boundaries[1] - Qx_boundaries[0]
    Qx_end = Qx_boundaries[-1] + Qx_step/100.

    assert axes[1].name() == 'Qy'
    Qy_axis = axes[1]
    Qy_boundaries = Qy_axis.binBoundaries().asNumarray()
    Qy_begin = Qy_boundaries[0]
    Qy_step = Qy_boundaries[1] - Qy_boundaries[0]
    Qy_end = Qy_boundaries[-1] + Qy_step/100.
 
    assert axes[2].name() == 'Qz'
    Qz_axis = axes[2]
    Qz_boundaries = Qz_axis.binBoundaries().asNumarray()
    Qz_begin = Qz_boundaries[0]
    Qz_step = Qz_boundaries[1] - Qz_boundaries[0]
    Qz_end = Qz_boundaries[-1] + Qz_step/100.

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
    binding.events2IQQQE_numpyarray(
        events, n,
        Qx_begin, Qx_end, Qx_step,
        Qy_begin, Qy_end, Qy_step,
        Qz_begin, Qz_end, Qz_step,
        E_begin, E_end, E_step,
        IQQQE.data().storage().asNumarray(),
        Ei,
        pixelpositions_ptr, ntotpixels, tofUnit, mod2sample,
        emission_time, intensity_npy_typecode)

    return IQQQE



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
