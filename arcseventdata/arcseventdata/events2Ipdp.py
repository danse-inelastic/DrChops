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


def events2Ipdp(events, n, Ipdp):
    axes = Ipdp.axes()
    assert len(axes) == 3
    assert axes[0].name() == 'detectorpackID'
    assert axes[1].name() == 'detectorID'
    assert len(axes[1].binCenters()) == 8
    assert axes[1].binCenters()[0] == 0
    assert axes[1].binCenters()[-1] == 7
    assert axes[2].name() == 'pixelID'
    assert len(axes[2].binCenters()) in [128, 256]
    import arcseventdata as binding
    return binding.events2Ipix_numpyarray(
        events, n, 0, Ipdp.size(), 1, Ipdp.data().storage().asNumarray() )


# version
__id__ = "$Id$"

#  End of file 
