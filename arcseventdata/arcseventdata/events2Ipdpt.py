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
    pixelIDs = Ipdpt.pixelID
    npixelbinsspertube = len(pixelIDs)
    assert 256 % npixelbinsspertube == 0
    pixelStep = pixelIDs[1]-pixelIDs[0]
    npixelspertube = npixelbinsspertube * pixelStep
    
    ntubesperpack = 8

    assert axes[3].name() == 'tof'
    tof_axis = axes[3]
    tof_boundaries = tof_axis.binBoundaries().asNumarray()
    tof_begin = tof_boundaries[0]
    tof_step = tof_boundaries[1] - tof_boundaries[0]
    tof_end = tof_boundaries[-1]

    ntotpixelbins = Ipdpt.size() / tof_axis.size()

    #make sure pack is continuous
    packs = Ipdpt.detectorpackID
    for i in range(len(packs)-1):
        assert packs[i] + 1 == packs[i+1]
        continue
    startpack = packs[0]
    assert startpack > 0, "pack should start at 1: %s" % startpack
    
    startpixelindex = (startpack-1)*ntubesperpack*npixelspertube
    endpixelindex = startpixelindex + ntotpixelbins*pixelStep

    maxpixelindex = endpixelindex
    
    import arcseventdata as binding
    return binding.events2Ipixtof_numpyarray(
        events, n,
        startpixelindex, endpixelindex, pixelStep,
        tof_begin, tof_end, tof_step,
        Ipdpt.data().storage().asNumarray(),
        maxpixelindex, tofUnit)


# version
__id__ = "$Id$"

#  End of file 
