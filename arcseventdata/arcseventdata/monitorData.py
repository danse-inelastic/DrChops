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


def readHistogram( filename ):
    s = open(filename).read()
    import numpy as N
    I = N.fromstring( s, 'u4' )
    n = len(I)
    tof = N.arange( 0, n, 1. )
    import histogram as H
    Itof = H.histogram(
        'I(tof)',
        [
        ('tof', tof),
        ],
        data = I, errors = I )
    return Itof


# version
__id__ = "$Id$"

#  End of file 
