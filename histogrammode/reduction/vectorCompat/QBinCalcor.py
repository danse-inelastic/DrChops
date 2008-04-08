#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.vectorCompat.QBinCalcor
## calculate Q bins out of phi bins
##
## only used by QRebinner

from reduction import reduction as red

class QBinCalc( object):
    """A simple class that encapsulates the QBinCalcor class in C++.
    """
    
    def datatype( self): return self._dtype

    def handle(self): return self._handle

    def incidentEnergy( self): return self._ei

    def __call__(self, ef, qBB):
        """my_QBinCalc( ef, qBinBounds) -> None
        Use a QBinCalc instance to compute the QBins for a given final
        energy.
        Inputs:
            ef (in meV, float)
            qBinBounds (reduction.datasets.StdVector instance to hold output)
        Output: None
        Exceptions: ValueError, TypeError
        Notes: Recognized datatypes:
            float....5
            double...6
        """
        if qBB.datatype() != self._dtype:
            errstr = 'qBinBounds (datatype=%s) must have same datatype as '+\
                     'QBinCalc (datatype=%s)'%( str(qBB.datatype()),
                                                str(self._dtype))
            raise TypeError, errstr
        red.QBinCalcor_Call( self._handle, self._dtype, ef, qBB.handle())
        return


    def __init__( self, phiBB, ei, inRadians=False):
        """QBinCalc( phiBinBounds, incidentEnergy, inRadians = False) ->
            new QBinCalc instance.
        Inputs:
            phiBinBounds: (constant phi bins, reduction.datasets.StdVector)
            incidentEnergy (in meV, float)
            inRadians ( true if angle bins in radians,
                otherwise assumed to be in degrees).
        Output: None
        See Also: __call__ 
        Exceptions: ValueError
        """

        if inRadians: inrad = 1
        else: inrad = 0
        self._handle = red.QBinCalcor( phiBB.handle(), phiBB.datatype(),
                                       ei, inrad)
        self._dtype = phiBB.datatype()
        self._ei = ei
        return


# version
__id__ = "$Id: QBinCalcor.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
