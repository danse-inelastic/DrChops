#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from numpy import *

class Functor:

    def __call__(self, *args, **kwds):
        raise NotImplementedError


class Gaussian(Functor):

    def __init__(self, x0, height, width ):
        self.x0 = x0
        self.height = height
        self.width = width
        return


    def __call__(self, x ):
        return self.height * exp( -( (x-self.x0)/self.width ) ** 2 )





# version
__id__ = "$Id$"

# End of file 
