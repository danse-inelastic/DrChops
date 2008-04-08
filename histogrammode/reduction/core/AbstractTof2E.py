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


## \package reduction.core.AbstactTof2E
## Abstract base class for reduction operators that
## converts I( *, tof) to I(*, E ).
##
##  * tof: time of flight
##  * E: energy of neutron (please note this is not the energy-transfer!)
##


import journal

debug = journal.debug( "reduction.core.AbstactTof2E")


class AbstractTof2E( object):

    """Convert time-of-flight to Energy of neutron
    (note: it is not Ei-Ef)

    Units:
      distance are in meters
      time are in microseconds
      energy are in milivolts

    """


    def __call__(self, inHist, outHist, distances):
        raise NotImplementedError


# version
__id__ = "$Id$"

# End of file
