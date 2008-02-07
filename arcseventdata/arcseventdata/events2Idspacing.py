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


def events2Idspacing(events, n, Idspacing, pixelpositions,
                     tofUnit = 1.e-7, mod2sample = 13.5):
    '''events2Idspacing(events, n, Idspacing, pixelpositions,
    npacks = 115, ndetsperpack = 8, npixelsperdet = 128,
    tofUnit = 1.e-7, mod2sample = 13.5) --> integrate events into Idspacing histogram

    events:
      neutron events
    n:
      number of neutron events
    Idspacing:
      I(d spacing) histogram. d spacing axis must have units attached
    pixelpositions:
      mapping pixels to positions
    tofUnit:
      unit of tof in pre-NeXus file
    '''
    axes = Idspacing.axes()
    assert len(axes) == 1
    daxis = axes[0]
    
    import units
    unit = daxis.unit()/units.length.angstrom
    boundaries = daxis.binBoundaries().asNumarray() * unit
    
    begin = boundaries[0]
    step = boundaries[1] - boundaries[0]
    end = boundaries[-1]

    ntotpixels = len( pixelpositions )

    from numpyext import getdataptr
    pixelpositions = getdataptr( pixelpositions )

    import arcseventdata as binding
    return binding.events2Idspacing_numpyarray(
        events, n, begin, end, step, Idspacing.data().storage().asNumarray(),
        pixelpositions, ntotpixels, tofUnit, mod2sample)


# version
__id__ = "$Id$"

#  End of file 
