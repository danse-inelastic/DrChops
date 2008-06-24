#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.histCompat.QRebinner
## rebin data in phi bins to Q bins
##
## this is a wrapper of reduction.vectorCompat.QRebinner


class QRebinner( object):

    def rebin( self, inHist, outHist, e_final):

        # should check units of inHist and outHist here!!!!
        # probably the right thing to do is to set the unit
        # of input histogram to a fixed unit and
        # set the output histogram to a fixed unit.
        import warnings
        message = (
            "A good strategy of dealing with units has not been implemented."
            "At this moment you have to take care of the units yourself."
            "For example, you can do"
            "  >>> rebin(inHist, outHist, e_final)"
            "  >>> outHist *= inHist.unit(), inHist.unit()*0"
            "Actually this is what is now implemented in reduction.core.Spe2Sqe"
            "Anyway, you should not need to use this class directly, "
            "You should use recored.core.Spe2Sqe or reduction.interactive.spe2sqe."
            )
        warnings.warn( message )

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
