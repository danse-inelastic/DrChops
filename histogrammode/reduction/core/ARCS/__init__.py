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


def solid_angles( ARCSxml = 'ARCS.xml', pixelradius = 1.27*cm, pixelheight = 100./128*cm):
    import arcseventdata as aed
    ii = aed.getinstrumentinfo( ARCSxml )
    pixelpositions = ii['pixelID-position mapping array']
    detaxes = ii['detector axes']
    from histogram import histogram
    solidangles = histogram( 'solid angles', detaxes )

    from SolidAngleCalculator import SolidAngleCalculator
    calculator = SolidAngleCalculator()
    calculator(solidangles.I, pixelpositions, pixelradius, pixelheight)
    return solidangles


from DetectorEfficiencyCalculator import deteff_hist


# version
__id__ = "$Id$"

# End of file 
