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

import reduction.units as units
cm = units.length.cm


def solid_angles( ARCSxml = 'ARCS.xml'):
    import arcseventdata as aed
    ii = aed.getinstrumentinfo( ARCSxml )
    solidangles = ii['solidangles']
    return solidangles


from DetectorEfficiencyCalculator import deteff_hist


# version
__id__ = "$Id$"

# End of file 
