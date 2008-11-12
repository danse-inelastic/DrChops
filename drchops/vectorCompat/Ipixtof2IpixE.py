#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import drchops.drchops as binding


bindings = {

    'double':binding.Itof2IE_batch_numpyarray,

    }


class Ipixtof2IpixE:
    
    """Rebin I(*,tof) to I(*, Ei-Ef) in batch mode

    only accepts numpy array.

    This rebinner deals with direct-geometry time-of-fligt inelastic neutron
    scattering instruments. It rebins tof to E=Ei-Ef.
    """

    def __init__(self):
        """Ipixtof2IpixE() -> engine to rebin I(tof) to I(Ei-Ef) in batch mode
        """
        return


    def __call__(
        self, 
        tofbb, Ipixtof, E2pixtof,
        ebb, IpixE, E2pixE,
        ei, mod2sample,
        distarr, 
        tmpEbb,
        ):
    
        """Ipixtof2IpixE(
        tofbb, Ipixtof, E2pixtof,
        ebb, IpixE, E2pixE,
        ei, mod2sample,
        distarr, 
        tmpEbb,
        ): rebin data in I[*,tof] to I[*,E]

    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      I[*,tof]:
        tofbb: tof bin boundaries
        Ipixtof: counts[*,tof] matrix   
        E2pixtof: error bar square of counts[*,tof] matrix
        
      I[*,E]:
        ebb: E bin boundaries
        IpixE: counts[*,E] matrix   
        E2pixE: error bar square of counts[*,E] matrix
        
      ei: incident energy (meV)
      mod2sample: moderator-to-sample distance (mm)

      Addtional info:
        distarr: distance[*] array

      Temporary arrays:
        tmpEbb: a temporary array. length >= len(tofbb)
      """
        arrayargs = [tofbb, Ipixtof, E2pixtof, 
                     ebb, IpixE, E2pixE,
                     distarr,
                     tmpEbb]
        for i, a in enumerate(arrayargs): arrayargs[i] = tonumarray( a )

        type = self._checkType( *arrayargs )
        engine = self._getEngine( type )

        args = arrayargs[:6] + [ei, mod2sample] + arrayargs[6:]
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


ipixtof2ipixE = Ipixtof2IpixE()


# version
__id__ = "$Id$"

# End of file 
