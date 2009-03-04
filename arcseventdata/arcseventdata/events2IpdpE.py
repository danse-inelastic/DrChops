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
    pixelIDs = IpdpE.pixelID
    npixelbinsspertube = len(pixelIDs)
    assert 256 % npixelbinsspertube == 0
    pixelStep = pixelIDs[1]-pixelIDs[0]
    npixelspertube = npixelbinsspertube * pixelStep

    ntubesperpack = 8

    assert axes[3].name() == 'energy'
    E_axis = axes[3]
    E_boundaries = E_axis.binBoundaries().asNumarray()
    E_begin = E_boundaries[0]
    E_step = E_boundaries[1] - E_boundaries[0]
    E_end = E_boundaries[-1]

    ntotpixelbins = IpdpE.size() / E_axis.size()

    #make sure pack is continuous
    packs = IpdpE.detectorpackID
    for i in range(len(packs)-1):
        assert packs[i] + 1 == packs[i+1]
        continue
    startpack = packs[0]
    assert startpack > 0, "pack should start at 1: %s" % startpack

    # 
    startpixelindex = (startpack-1)*ntubesperpack*npixelspertube
    endpixelindex = startpixelindex + ntotpixelbins*pixelStep

    maxpixelindex = endpixelindex

    #
    from numpyext import getdataptr
    pixelpositions = getdataptr( pixelpositions )
    
    import arcseventdata as binding
    return binding.events2IpixE_numpyarray(
        events, n,
        startpixelindex, endpixelindex, pixelStep,
        E_begin, E_end, E_step,
        IpdpE.data().storage().asNumarray(),
        Ei,
        pixelpositions, maxpixelindex, tofUnit, mod2sample,
        emission_time)


# version
__id__ = "$Id$"

#  End of file 
