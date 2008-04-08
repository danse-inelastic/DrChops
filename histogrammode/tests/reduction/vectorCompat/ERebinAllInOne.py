#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from rebin import rebin

from reduction.utils import conversion 


def ERebinAllInOne(ei, distMod2Sample, tofs, distSample2Pixel, es, dataInTofBins):
    #ei: meV
    #distMod2Sample: m
    #tofs: mu seconds
    #distSample2Pixel: m
    distMod2Sample/conversion.e2v(ei)
    from numpy import array
    tofs = array (tofs)
    toffs = tofs-distMod2Sample/conversion.e2v(ei)*1e6 # mu seconds
    vfs = distSample2Pixel*1e6/toffs # m/s
    efs=[ conversion.v2e( vf ) for vf in vfs]
    es_converted = ei-array(efs)
    return rebin (es_converted, dataInTofBins, es)




def test():
    numTBins = 9
    numEBins = 9
    e_i = 276.5
    mod2SampDist = 20.1
    dt = 50.0
    de = 10.0
    tofs = [3000.0 + i*dt for i in range(numTBins+1)]
    import math
    distance = math.sqrt( 4.0**2+0.00005**2)
    nrgs = [-50.0 + i*de for i in range(numEBins+1)]
    data = [1.0 for i in range(numTBins) ]
    print ERebinAllInOne( e_i, mod2SampDist, tofs, distance, nrgs, data )
    return 




if __name__ == "__main__": test()
    


# version
__id__ = "$Id: getDetInfo.py 809 2006-02-27 07:42:46Z linjiao $"

# End of file 
