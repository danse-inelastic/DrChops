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


from drchops.vectorCompat.Ipixtof2IpixE import ipixtof2ipixE as vengine


import journal
debug = journal.debug( 'drchops.histCompat.Ipixtof2IpixE' )


def Ipixtof2IpixE(
    Ipixtof,
    ei, mod2sample, 
    dist_pix,
    IpixE = None,
    Eaxis = None,
    ):
    
    """Ipixtof2IpixE(Ipixtof, ei, mod2sample, dist_pix, IpixE=None):
    Rebin I(*,tof) to I(*, Ei-Ef) in batch mode

    This rebinner deals with direct-geometry time-of-fligt inelastic neutron
    scattering instruments. It rebins tof to E=Ei-Ef.
    
    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      Ipixtof: I[*,tof] histogram

      ei: incident energy (with explicit unit)
      mod2sample: moderator-to-sample distance (with explicit unit)
      dist_pix: distance[*] (histogram, unit must be specified)

      Addtional arrays:
        IpixE: I[*,E] histogram (optional)

    All input should be either histograms or physical quantities with units
    """

    # make sure input histogram has the right unit
    Iunit = Ipixtof.unit()
    try: Iunit + 1
    except: raise RuntimeError("intensities of I(*,tof) histogram should be unitless")

    import drchops.units as units
    microsecond = units.time.microsecond
    mm = units.length.mm
    meV = units.energy.meV

    #pixaxis = Ipixtof.axisFromName('pixelID')
    pixaxes = Ipixtof.axes()[:-1]
    tofaxis = Ipixtof.axisFromName('tof')
    tofbb = tofaxis.binBoundaries() * (tofaxis.unit()/microsecond)

    mod2sample = mod2sample/mm
    
    Iptmat = Ipixtof.data().storage()
    E2ptmat = Ipixtof.errors().storage()

    if IpixE is None:
        if Eaxis is None:
            raise ValueError("Neither IpixE nor Eaxis is supplied")
        from histogram import histogram
        IpixE = histogram('I(pix,E)', pixaxes+[Eaxis])
    else:
        Eaxis = IpixE.axisFromName('energy')
    ebb = Eaxis.binBoundaries()

    Ipemat = IpixE.data().storage()
    E2pemat = IpixE.errors().storage()

    distarr = dist_pix.data().storage()
    distarr *= dist_pix.unit()/mm
    
    tmpEbb = tofbb.copy()

    ei = ei/meV
    
    args = [tofbb, Iptmat, E2ptmat,
            ebb, Ipemat, E2pemat,
            ei, mod2sample, 
            distarr,
            tmpEbb,
            ]

    debug.log( '%s' % args )
    
    vengine( *args )

    IpixE *= Iunit, 0
    
    return IpixE


#debug.activate()

# version
__id__ = "$Id$"

# End of file 
