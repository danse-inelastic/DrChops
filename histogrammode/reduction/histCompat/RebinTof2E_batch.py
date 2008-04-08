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


from reduction.vectorCompat import RebinTof2E_batch as vRebinDrivers


import journal
debug = journal.debug( 'reduction.histCompat.RebinTof2E_batch' )


def istartof2IE(
    I_startof, I_E,
    dist_star, mask_star):
    
    """istartof2IE(I_startof, I_E, dist_star, mask_star) -> None
    rebin I(*,tof) to I(Ef) for each pixel and add them all together

    This rebinner converts I(tof) to I(E). Tof is time of fligt
    from some source to a pixel. By knowing the distance between
    the source and the pixel, it is easy to calculate a neutron's
    velocity and hence its energy.
    This rebinner goes through a list of pixels and converts
    I(tof) for each pixel to I(E) and add I(E) to a sum.
    
    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      I_startof: I[*,tof]:
        
      I_E: I[E]

      Addtional arrays:
        mask_star: mask[*]: mask histogram.
        dist_star: distance[*] (histogram, unit must be specified)

    All input should be either histograms or numbers with units
    """

    from pyre.units.time import microsecond
    from pyre.units.length import mm
    from pyre.units.energy import meV
    from pyre.units.angle import degree

    tofaxis = I_startof.axisFromName('tof')
    tofaxis.changeUnit( 'microsecond' )
    tofbb = tofaxis.binBoundaries()

    cntsmat = I_startof.data().storage()
    err2mat = I_startof.errors().storage()

    Eaxis = I_E.axisFromName( 'energy' )
    Eaxis.changeUnit( 'meV' )
    ebb = Eaxis.binBoundaries()
    I_E_data = I_E.data().storage()
    I_E_err2 = I_E.errors().storage()

    maskarr = mask_star.data().storage()
    distarr = dist_star.data().storage()
    distarr *= dist_star.unit()/mm
    
    tmpEbb = tofbb.copy()
    tmpI = ebb.copy()[:-1]
    
    args = [tofbb, cntsmat, err2mat, 
            ebb, I_E_data, I_E_err2,
            distarr, maskarr, 
            tmpEbb, tmpI]

    debug.log( '%s' % args )
    
    return vRebinDrivers.istartof2IE( *args )


#debug.activate()

# version
__id__ = "$Id$"

# End of file 
