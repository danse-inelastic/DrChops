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


from reduction.vectorCompat.DGTS_RebinTof2E_batch import dgts_RebinTof2E_batch \
     as vengine


import journal
debug = journal.debug( 'reduction.histCompat.DGTS_RebinTof2E_batch' )


def dgts_RebinTof2E_batch(
    I_startof, S_pe, sa_p,
    ei, mod2sample, 
    mask_star, phi_star, sa_star,
    dist_star,
    radius_star, pressure_star,
    ):
    
    """dgts_RebinTof2E_batch(I_startof, S_pe, ei, mod2sample,
    mask_star, phi_star, dist_star): Rebin I(*,tof) to I(phi, Ei-Ef) in \
    batch mode

    This rebinner deals with direct-geometry time-of-fligt inelastic neutron
    scattering instruments. It rebins tof to E=Ei-Ef.
    
    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      I_startof: I[*,tof]:
        
      S_pe: S[phi,E]
      sa_p: solid_angle[phi]
        
      ei: incident energy (with explicit unit)
      mod2sample: moderator-to-sample distance (with explicit unit)

      Addtional arrays:
        mask_star: mask[*] 
        phi_star: phi[*]
        sa_star: solid_angle[*]
        dist_star: distance[*] (histogram, unit must be specified)
        radius_star: radius[*] (histogram, unit must be specified)
        pressure_star: pressure[*] (histogram, unit must be specified)

    All input should be either histograms or floats
    """

    from pyre.units.time import microsecond
    from pyre.units.length import mm,cm
    from pyre.units.pressure import atm
    from pyre.units.energy import meV
    from pyre.units.angle import degree

    tofaxis = I_startof.axisFromName('tof')
    tofaxis.changeUnit( 'microsecond' )
    tofbb = tofaxis.binBoundaries()

    mod2sample /= mm
    
    cntsmat = I_startof.data().storage()
    err2mat = I_startof.errors().storage()

    phibb = S_pe.axisFromName( 'phi' ).binBoundaries()
    ebb = S_pe.axisFromName( 'energy' ).binBoundaries()
    S = S_pe.data().storage()
    Serr2 = S_pe.errors().storage()
    intsa = sa_p.data().storage()

    maskarr = mask_star.data().storage()
    phiarr = phi_star.data().storage() * (phi_star.unit()/degree)
    saarr = sa_star.data().storage()
    distarr = dist_star.data().storage()
    distarr *= dist_star.unit()/mm
    radiusarr = radius_star.data().storage()
    radiusarr *= radius_star.unit()/cm
    pressurearr = pressure_star.data().storage()
    pressurearr *= pressure_star.unit()/atm

    tmpEbb = tofbb.copy()
    tmpI = ebb.copy()[:-1]

    ei/=meV
    
##     print tofbb.asNumarray()
##     print phibb.asNumarray()
##     print ebb.asNumarray()
##     print cntsmat.asNumarray()
##     print err2mat.asNumarray()
##     print ei, mod2sample
##     print maskarr.asNumarray()
##     print phiarr.asNumarray()
##     print saarr.asNumarray()
##     print distarr.asNumarray()

    args = [tofbb, cntsmat, err2mat, 
            phibb, ebb, S, Serr2, intsa,
            ei, mod2sample, 
            maskarr, phiarr, saarr, distarr,
            radiusarr, pressurearr,
            tmpEbb, tmpI]

    debug.log( '%s' % args )
    
    return vengine( *args )


#debug.activate()

# version
__id__ = "$Id$"

# End of file 
