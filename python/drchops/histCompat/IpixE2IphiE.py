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


from drchops.vectorCompat.IpixE2IphiE import ipixtof2ipixE as vengine


import journal
debug = journal.debug( 'drchops.histCompat.IpixE2IphiE' )


def IpixE2IphiE(
    IpixE,
    phi_pix, solidangle_pix, mask_pix,
    IphiE = None,
    solidangle_phi = None,
    phiaxis = None,
    ):
    
    """IpixE2IphiE(IpixE, phi_pix, solidangle_pix, mask_pix,
    IphiE = None, solidangle_phi = None, phiaxis = None,):
    Rebin I(pix,E) to I(phi, E) 

    I[pix,E]: data to be reduced.

    inputs:
      IpixE: I[pix,E] histogram

      phi_pix, solidangle_pix, mask_pix: phi[pix], solidangle[pix], mask[pix]

    outputs
      IphiE: I[phi,E] histogram
      solidangle_phi: solidangle[phi] histogram

    All input should be either histograms or physical quantities with units
    """

    # make sure input histogram has the right unit
    Iunit = IpixE.unit()
    try: Iunit + 1
    except: raise RuntimeError("intensities of I(*,tof) histogram should be unitless")

    import drchops.units as units
    degree = units.angle.degree
    meV = units.energy.meV

    pixaxis = IpixE.axisFromName('pixelID')
    Eaxis = IpixE.axisFromName('energy')
    ebb = Eaxis.binBoundaries() * (Eaxis.unit()/meV)

    IpixEmat = IpixE.data().storage()
    E2pixEmat = IpixE.errors().storage()

    if IphiE is None:
        if phiaxis is None:
            raise ValueError("Neither IphiE nor phiaxis is supplied")
        from histogram import histogram
        IphiE = histogram('I(phi,E)', [phiaxis, Eaxis])
    else:
        phiaxis = IphiE.axisFromName('phi')
    phibb = phiaxis.binBoundaries() * (phiaxis.unit()/degree)

    if solidangle_phi is None:
        from histogram import histogram
        solidangle_phi = histogram('solidangle(phi)', [phiaxis])

    IphiEmat = IphiE.data().storage()
    E2phiEmat = IphiE.errors().storage()

    sa = solidangle_phi.data().storage()
    saE2 = solidangle_phi.errors().storage()

    phiarr = phi_pix.data().storage() * (phi_pix.unit()/degree)
    saarr = solidangle_pix.data().storage(); saE2arr = solidangle_pix.errors().storage()
    maskarr = mask_pix.I    
    
    args = [ebb, IpixEmat, E2pixEmat,
            phibb, IphiEmat, E2phiEmat, sa, saE2,
            phiarr, saarr, saE2arr, maskarr,
            ]

    debug.log( '%s' % args )
    
    vengine( *args )

    IphiE *= Iunit, 0
    
    return IphiE, solidangle_phi


#debug.activate()

# version
__id__ = "$Id$"

# End of file 
