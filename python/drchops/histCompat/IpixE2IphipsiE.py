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


from drchops.vectorCompat.Zt2Zxy import zt2zxy


import journal
debug = journal.debug( 'drchops.histCompat.IpixE2IphipsiE' )


def IpixE2IphipsiE(
    IpixE,
    phi_pix, psi_pix, solidangle_pix, mask_pix,
    IphipsiE = None,
    solidangle_phipsi = None,
    phiaxis = None, psiaxis = None
    ):
    
    """IpixE2IphipsiE(IpixE, phi_pix, psi_pix, solidangle_pix, mask_pix,
    IphipsiE = None, solidangle_phipsi = None, phiaxis = None, psiaxis=None):
    Rebin I(pix,E) to I(phi, psi, E) 

    inputs:
      IpixE: I[pix,E] histogram

      phi_pix, psi_pix, solidangle_pix, mask_pix: phi[pix], psi[pix], solidangle[pix], mask[pix] histograms

      (optional) phiaxis, psiaxis: axes for the output histogram. If IphipsiE is supplied as a keyword arugment to this function, phiaxis and psiaxis are automatically obtained from the IphipsiE histogram.
      
    outputs
      (optional) IphipsiE: I[phi,psi,E] histogram. This histogram will be created for you if you don't supply one. But you will need to specify phiaxis and psiaxis.
      (optional) solidangle_phipsi: solidangle[phi,psi] histogram. This histogram will be created for you if you don't supply one. But you will need to specify phiaxis and psiaxis.

    All inputs should be either histograms or physical quantities with units
    """

    # make sure input histogram has the right unit
    import drchops.units as units
    degree = units.angle.degree
    meV = units.energy.meV

    Iunit = IpixE.unit()
    try: Iunit + 1
    except: raise RuntimeError("intensities of I(*,tof) histogram should be unitless")
    #
    saunit = solidangle_pix.unit()
    try: saunit + 1
    except: raise RuntimeError('solid angle histogram should be unitless')

    pixaxis = IpixE.axisFromName('pixelID')
    Eaxis = IpixE.axisFromName('energy')

    if IphipsiE is None:
        if phiaxis is None or psiaxis is None:
            raise ValueError("Neither IphipsiE nor (phiaxis,psiaxis) is supplied")
        from histogram import histogram
        IphipsiE = histogram('I(phi,psi,E)', [phiaxis, psiaxis, Eaxis])
    else:
        phiaxis = IphipsiE.axisFromName('phi')
        psiaxis = IphipsiE.axisFromName('psi')
    #
    phibb = phiaxis.binBoundaries() * (phiaxis.unit()/degree)
    psibb = psiaxis.binBoundaries() * (psiaxis.unit()/degree)

    if solidangle_phipsi is None:
        from histogram import histogram
        solidangle_phipsi = histogram('solidangle(phi, psi)', [phiaxis, psiaxis])

    def Zpix2Zphipsi(zpix, zphipsi):
        phipix = phi_pix.I
        psipix = psi_pix.I
        maskpix = mask_pix.I
        zt2zxy(phipix, psipix, zpix, maskpix,
               phibb, psibb, zphipsi)
        return

    # tmp array
    import numpy
    zphipsi = numpy.zeros(solidangle_phipsi.shape(), dtype='d')
    zphipsiE = numpy.zeros(IphipsiE.shape(), dtype='d')

    def ZpixE2ZphipsiE(zpixE, zphipsiE):
        shape = zpixE.shape
        edim = shape[-1]
        for i in range(edim):
            zphipsi[:] = 0
            Zpix2Zphipsi(zpixE[:, i], zphipsi)
            zphipsiE[:,:, i] = zphipsi
            continue
        return
    # intensity in IpixE
    zphipsiE[:] = 0
    ZpixE2ZphipsiE(IpixE.I*Iunit, zphipsiE)
    IphipsiE.I = zphipsiE
    # error^2 in IpixE
    zphipsiE[:] = 0
    ZpixE2ZphipsiE(IpixE.E2*Iunit*Iunit, zphipsiE)
    IphipsiE.E2 = zphipsiE
    
    # "intensity" in solidangle_phipsi
    zphipsi[:] = 0
    Zpix2Zphipsi(solidangle_pix.I*saunit, zphipsi)
    solidangle_phipsi.I = zphipsi
    # error^2 in solidangle_phipsi
    zphipsi[:] = 0
    Zpix2Zphipsi(solidangle_pix.E2*saunit*saunit, zphipsi)
    solidangle_phipsi.E2 = zphipsi

    return IphipsiE, solidangle_phipsi


#debug.activate()

# version
__id__ = "$Id$"

# End of file 
