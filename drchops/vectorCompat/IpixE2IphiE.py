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

    'double':binding.IpixE2IphiE_numpyarray,

    }


class IpixE2IphiE:
    
    """Rebin I(pix,E) to I(phi,E)

    only accepts numpy array.
    """

    def __init__(self):
        """IpixE2IphiE() -> engine to rebin I(pix,E) to I(phi,E) in batch mode
        """
        return


    def __call__(
        self, 
        ebb, IpixE, E2pixE,
        phibb, IphiE, E2phiE, solidanglephi, solidangleE2phi,
        phiarr,
        saarr, saE2arr,
        maskarr,
        ):
    
        """IpixE2IphiE(
        ebb, IpixE, E2pixE,
        phibb, IphiE, E2phiE, solidanglephi, solidangleE2phi,
        phiarr,
        saarr, saE2arr,
        maskarr,
        ): rebin data in I(pix,E) to I(phi,E)

    inputs:
      I[pix,E]:
        ebb: energy bin boundaries
        IpixE: counts[pixel,E] matrix   
        E2pixE: error bar square of counts[pixel,E] matrix
        
      I[phi,E]:
        phibb: phi bin boundaries
        IphiE: counts[phi,E] matrix   
        E2phiE: error bar square of counts[phi,E] matrix

      solidangle[phi]:
        solidanglephi
        solidangleE2phi
        
      phiarr: phi[pixel] array
      saarr, saE2arr: solidangle[pixel] array and error bar squares
      maskarr: mask[pixel] array
      """
        arrayargs = [ebb, IpixE, E2pixE,
                     phibb, IphiE, E2phiE, solidanglephi, solidangleE2phi,
                     phiarr, saarr, saE2arr]
        for i, a in enumerate(arrayargs): arrayargs[i] = tonumarray( a )

        type = self._checkType( *arrayargs )
        engine = self._getEngine( type )

        args = arrayargs + [maskarr]
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

    pass # end of IpixE2IphiE


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


ipixtof2ipixE = IpixE2IphiE()


# version
__id__ = "$Id$"

# End of file 
