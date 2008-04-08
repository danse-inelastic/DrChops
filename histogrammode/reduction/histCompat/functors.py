#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import numpy as N


class Gaussian:

    def __init__(self, bg, ht, center, width):
        self.bg = bg
        self.ht = ht
        self.center = center
        self.width = width
        return

    
    def __call__(self, x):
        a0 = self.bg
        a1 = self.ht
        a2 = self.center
        a3 = self.width
        return a0 + a1 * N.exp( - ((x-a2)/a3)**2 )


    pass # end of Gaussian

# version
__id__ = "$Id$"

# End of file 
