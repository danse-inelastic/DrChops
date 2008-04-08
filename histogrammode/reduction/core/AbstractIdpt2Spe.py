#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.AbstractIdpt2Spe
## Provides abstract base class for S(phi,E) reducers that
## reduce I(det, pix, tof) to S(phi, E).
##
## Names of all subclasses should contain the string "Idpt2Spe".


class AbstractIdpt2Spe:


    """ reduce I(det, pix, tof) to S(phi,E) histogram

    This is the abstact base class of reducers that reduce
    I(det, pix, tof) to S(phi,E) histogram
    """


    def __call__(self,  ei, Idpt, instrument, geometer,
                 phiAxis=None, EAxis=None, mask = None):
        """reduce I(det, pix, tof) to S(phi,E) histogram

        \arg ei incident neutron energy
        \arg Idpt histogram (I(det,pix,tof)) to be reduced
        \arg instrument instrument python representation
        \arg geometer geometer who measures distances, angles, etc
        """
        raise NotImplementedError , "%s must override __call__" % (
            self.__class__.__name__)


# version
__id__ = "$Id: AbstractIdpt2Spe.py 1146 2006-09-27 17:31:51Z linjiao $"

# End of file 
