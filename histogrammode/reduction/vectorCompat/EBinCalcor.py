#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

##\package reduction.vectorCompat.EBinCalcor
## calculate energy bins out of time-of-flight bins
##
## only used by reduction.vectorCompat.ERebinAllInOne

from reduction import reduction as red
from TemplateCObject import TemplateCObject

class EBinCalcor(TemplateCObject):
    """EBinCalc( ei, mod2samp)->New EBinCalc object.
    Create a new energy bin calculator.
    inputs:
        incidentEnergy: in meV; float)
        modSampDist: distance from moderator to sample, in mm; (float)
    output:
        EBinCalcor instance of type <datatype> (PyCObject)
    Exceptions:
    Notes:  Datatype is taken from time bins vector."""
    
    def __call__(self, pixelDist, tbbVec, ebbVec):
        """ebincalcInstance( pixelDist, tBinBoundsVec, eBinBoundsVec) -> None
        Calculate energy bin boundaries of time bin boundaries for a given pixel.
        inputs:
            pixelDist: distance from sample to pixel (float)
            tBinBoundsVec (instance of StdVector)
            eBinBoundsVec (instance of StdVec)
        outputs:
            None (results stored in eBinBoundsVec)
        Exceptions: ValueError, RuntimeError
        """
        try:
            red.EBinCalcor_Call( self._handle, self._templateType, pixelDist,
                                 tbbVec._handle, ebbVec._handle)
        except RuntimeError, msg:
            print "Caught RuntimeError: %s" % msg
            print tbbVec.__class__.__name__, "vector datatype: ", \
                  tbbVec.datatype()
            print "EBinCalcor datatype: %s" % self.datatype()
            raise RuntimeError, msg
        return

    
    def __init__(self, datatype, ei, mod2samp):
        """EBinCalcor( datatype, e_i, mod2sampDist) -> new instance
        Create new instance to compute energy bin bounds given time bn bounds.
        Inputs:
            datatype: type code (int)
            e_i: incident energy in meV (float)
            mod2sampDist: distance from moderator to sample in mm (float)
        Output:
            new instance
        Exceptions: ValueError
        Notes: (1) ValueError raised if inappropriate type code. Recognized
        types are:
            5........float
            6........double
        (2) Handle kept as TWrapper."""
        datatype
        handle = red.EBinCalcor( datatype, ei, mod2samp)
        # from EBinCalcor_bdgs.cc: 
        classID = 490315662

        TemplateCObject.__init__( self, datatype, handle, "EBinCalcor",classID)

        return


# version
__id__ = "$Id: EBinCalcor.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
