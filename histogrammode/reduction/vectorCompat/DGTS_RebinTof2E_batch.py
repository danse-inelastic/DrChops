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

import reduction.reduction as binding


bindings = {

    'double':binding.DGTS_RebinTof2E_batch_numpyarray,

    }


class DGTS_RebinTof2E_batch:
    
    """Rebin I(*,tof) to I(phi, Ei-Ef) in batch mode

    only accepts numpy array.

    This rebinner deals with direct-geometry time-of-fligt inelastic neutron
    scattering instruments. It rebins tof to E=Ei-Ef.
    """

    def __init__(self):
        """DGTS_RebinTof2E_batch() -> engine to rebin I(tof) to I(Ei-Ef) in batch mode
        """
        return


    def __call__(
        self, 
        tofbb, cntsmat, err2mat, 
        phibb, ebb, S, Serr2, intsa,
        ei, mod2sample, 
        maskarr, phiarr, saarr, distarr,
        radiusarr, pressurearr,
        tmpEbb, tmpI):
    
        """dgts_RebinTof2E_batch( 
    tofbb, cntsmat, err2mat, 
    phibb, ebb, S, Serr2, 
    ei, mod2sample, 
    maskarr, phiarr, distarr,
    radiusarr, pressurearr,
    tmpEbb, tmpI): rebin data in I[*,tof] to S[phi,E]

    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      I[*,tof]:
        tofbb: tof bin boundaries
        cntsmat: counts[*,tof] matrix   
        err2mat: counts_err2[*,tof] matrix
        
      S[phi,E]:
        phibb: phi bin boundaries 
        ebb: e bin boundaries 
        S: S[phi,E] matrix  
        Serr2: Serr2[phi,E] matrix
        intsa: integrated_solid_angle[phi]
        
      ei: incident energy (meV)
      mod2sample: moderator-to-sample distance (mm)

      Addtional info:
        maskarr: mask[*] array
        phiarr: phi[*] array
        saarr: solid_angle[*] array
        distarr: distance[*] array
        radiusarr: radius[*] array
        pressurearr: pressure[*] array

      Temporary arrays:
        tmpE: a temporary array. length = len(tofbb) 	
        tmpI: a temporary array. length = len(ebb)-1   
      """
        maskarr = tonumarray( maskarr )
        from numpy import array
        maskarr = array( maskarr, 'i' )
        
        arrayargs = [tofbb, cntsmat, err2mat, 
                     phibb, ebb, S, Serr2, intsa,
                     phiarr, saarr, distarr,
                     radiusarr, pressurearr,
                     tmpEbb, tmpI]
        for i, a in enumerate(arrayargs): arrayargs[i] = tonumarray( a )

        type = self._checkType( *arrayargs )
        engine = self._getEngine( type )

        args = arrayargs[:8] + [ei, mod2sample, maskarr] + arrayargs[8:]
        return engine( *args )


    def _checkType(self, *args):
        for a in args:
            import numpy
            types = [numpy.double]
            assert a.dtype.type in types, "wrong data type: %s" % a.dtype
            continue
        return 'double'
        #raise NotImplementedError


    def _getEngine(self, type):
        return bindings[ type ]

    pass # end of DGTS_RebinTof2E_batch


def tonumarray( a ):
    from ndarray.AbstractNdArray import NdArray
    import numpy
    if isinstance(a, NdArray):
        ret = a.asNumarray()
    elif isinstance(a, numpy.ndarray):
        ret = a
    else:
        #try to create a new array
        ret = numpy.array( a )
        pass 
    #ret.shape = -1,
    return ret


dgts_RebinTof2E_batch = DGTS_RebinTof2E_batch()


# version
__id__ = "$Id$"

# End of file 
