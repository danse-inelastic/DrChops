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


class Istartof2IE:
    
    """Rebin I(tof) to I(Ef) for each pixel and add them all together

    only accepts numpy array.

    This rebinner deals with the cases where we can assume 
    that the each neutron is moving in a constant speed.
    So we can infer neutron energy from time-of-flight.
    """

    bindings = {

        'double': binding.Istartof2IE_numpyarray,
        
        }


    def __init__(self):
        """Istartof2IE() -> engine to rebin I(tof) to I(Ef) for
        all pixels and add them together.
        """
        return


    def __call__(
        self, 
        tofbb, Itof, Itof_err2, 
        ebb, I_E, I_E_err2, 
        distarr, maskarr, 
        tmpEbb, tmpI):
    
        """istartof2IE( 
    tofbb, Itof, Itof_err2, 
    ebb, I_E, I_E_err2, 
    distarr, maskarr, 
    tmpEbb, tmpI): rebin data in I[*,tof] to I[E]

    I[*,tof]: data to be reduced. * can be regarded as pixel axis

    inputs:
      I[*,tof]:
        tofbb: tof bin boundaries
        Itof: counts[*,tof] matrix   
        Itof_err2: counts_err2[*,tof] matrix
        
      I[E]:
        ebb: e bin boundaries 
        I_E: I[E] 
        I_E_err2: I_E_err2[E] 
        
      Addtional info:
        distarr: distance[*] array
        maskarr: mask[*] array

      Temporary arrays:
        tmpE: a temporary array. length = len(tofbb) 	
        tmpI: a temporary array. length = len(ebb)-1   
      """
        maskarr = tonumarray( maskarr )
        from numpy import array
        maskarr = array( maskarr, 'i' )
        
        arrayargs = [tofbb, Itof, Itof_err2, 
                     ebb, I_E, I_E_err2, 
                     distarr, 
                     tmpEbb, tmpI]
        for i, a in enumerate(arrayargs): arrayargs[i] = tonumarray( a )

        type = self._checkType( *arrayargs )
        engine = self._getEngine( type )

        args = arrayargs[:7] + [maskarr] + arrayargs[7:]
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
        return self.bindings[ type ]

    pass # end of Istartof2IE


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


istartof2IE = Istartof2IE()


# version
__id__ = "$Id$"

# End of file 
