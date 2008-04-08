
def _makeMsliceHists(self, detIDs, histCollection):
    """ create histograms of I(det, pxl, energy), phi(det,pxl), psi(det,pxl)
    """
    detIDs = list(detIDs) # I just want a copy
    detIDs.sort()
    det = ( "detectorID", detIDs )
    pxlIDs = []
    for hist in histCollection.getAll():
        pxlAxis = hist.pixelAxis()
        for pxlID in pxlAxis.binCenters():
            if pxlID not in pxlIDs: pxlIDs.append( pxlID )
            continue
        continue
    pxlIDs.sort()
    pxl = ( "pixelID", pxlIDs )
    emin, de, ne = self.emin, self.de, self.numEBins 
    import numpy as N
    E   = ( "energy", N.arange( emin, emin + ne*de, de ) )

    shape = (len(detIDs), len(pxlIDs), ne)
    shape1 = (len(detIDs), len(pxlIDs)) 
    from histogram import histogram
    I_pde =  histogram( "I_dpe", [det, pxl, E] )
    phi_dp = histogram( "phi_dp", [det,pxl])
    psi_dp = histogram( "psi_dp", [det,pxl])

    self._debug.log( "det = %s, pxl = %s, E = %s" % (
        det, pxl, E) )
    return I_pde, phi_dp, psi_dp

