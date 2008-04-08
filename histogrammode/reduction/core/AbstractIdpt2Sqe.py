#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.AbstractIdpt2Sqe
## provides base class for S(Q,E) reducers that
## reduce I(det, pix, tof) to S(Q, E).
##


class AbstractIdpt2Sqe:


    """Reduce I(det, pix, tof) to S(scalar Q,E)
    """


    def __call__(self, ei, Idpt, instrument, geometer,
                 QAxis = None, EAxis = None, mask=None, **kwds):
        """reduce I(det, pix, tof) to S(scalar Q,E) histogram
        
        Idpt: I(det, pix, tof) histogram
        EAxis: energy axis
        QAxis: q axis
        ei: incident energy
        mask: detector mask
        """
        raise NotImplementedError


# version
__id__ = "$Id$"

# End of file 
