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


## After events are gather into a I(Q,E) histogram, we need
## to normalize the histogram by the solid angle.
## So we will need a "histogram", solid_angle(Q, E).
##


def calcSolidAngleQE( ei, qaxis, eaxis, pixelpositions, mask_function):
    from numpy import array
    one = array( (1,0) )
    
    from histogram import histogram
    sa = histogram( 'solid_angle', [ qaxis, eaxis ] )
    
    ntotpixels = len(pixelpositions)
    for e in eaxis.binCenters():
        for pixelID in range( ntotpixels ):
            if mask_function( pixelID ): continue

            position = pixelpositions[ pixelID ]
            q = calcQ( position, ei, e )
            
            # number of pixels. should be solid angle
            # need reimplement this in the future
            sa[ q,e ] += one

            continue
        continue
    return sa


def calcQ( position, ei, e ):
    ef = ei - e
    # q**2 = ki**2 + kf**2 - 2ki*kf*cos(theta)
    # cos(theta) = x/r
    x,y,z = position
    r = nl.norm( position )
    cost = x/r
    q2inmev = ei + ef - 2 * sqrt(ei)*sqrt(ef) * cost
    q = sqrt( q2inmev ) * SE2Q
    return q


import numpy.linalg as nl
from numpy import sqrt
    

V2K = 1.58801E-3; # Convert v[m/s] to k[1/AA]
K2V = 1./V2K; # Convert k[1/AA] to v[m/s] 
SE2V = 437.3949;  # Convert sqrt(E)[meV] to v[m/s]
SE2Q = SE2V * V2K

# version
__id__ = "$Id$"

#  End of file 
