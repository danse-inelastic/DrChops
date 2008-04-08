#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.histCompat.QRebinner
## rebin data in phi bins to Q bins
##
## this is a wrapper of reduction.vectorCompat.QRebinner


class QRebinner( object):

    def rebin( self, inHist, outHist, e_final):

        # should check units of inHist and outHist here!!!!

        indata = inHist.data().storage()
        inerrs = inHist.errors().storage()
        outdata = outHist.data().storage()
        outerrs = outHist.errors().storage()

        e_final = e_final/meV
        
        self._rebinner( e_final, indata, outdata, inerrs, outerrs)

        return


    def __init__( self, sphiEHist, ei, QAxis):

        ei = ei/meV

        phiAxis = sphiEHist.axisFromName( 'phi' )

        phiBB = _convertUnit(
            phiAxis.storage(), phiAxis.unit(), degree )
        dphi = phiBB[1] - phiBB[0]

        qbbNew = _convertUnit(
            QAxis.storage(), QAxis.unit(), 1./angstrom )

        #print phiBB.asList(), dphi, ei, qbbNew.asList()
        from reduction.vectorCompat.QRebinner import QRebinner
        self._rebinner = QRebinner( phiBB, dphi, ei, qbbNew, phiInRadians = False)
        
        return
    
    
def _convertUnit( array, originalUnit, destinationUnit ):
    if originalUnit == destinationUnit: return array # to speed up
    return array * (originalUnit/destinationUnit)


from pyre.units.energy import meV
from pyre.units.angle import degree
from pyre.units.length import angstrom

# version
__id__ = "$Id: QRebinner.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
