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

    'double':binding.Zt2Zxy_numpyarray,

    }


class Zt2Zxy:
    
    """Rebin Z(t) to Z(x,y)

    only accepts numpy array.
    """

    def __init__(self):
        """Zt2Zxy() -> engine to rebin Z(t) to Z(x,y)
        """
        return


    def __call__(
        self,
        xt, yt, zt, maskt,
        outxbb, outybb,
        outzxy,
        ):
    
        """Zt2Zxy(
        xt, yt, zt, maskt,
        outxbb, outybb,
        outzxy,
        ): rebin data in Z(t) to Z(x,y)

    inputs:
      xt, yt, zt, maskt: x(t), y(t), z(t), mask(t)
      outxbb/outybb: x/y bin boundaries for outputs
      outzxy: z(x,y)
      """
        arrayargs = [xt, yt, zt,
                     outxbb, outybb,
                     outzxy]
        for i, a in enumerate(arrayargs): arrayargs[i] = tonumarray( a )

        type = self._checkType( *arrayargs )
        engine = self._getEngine( type )

        args = arrayargs[:3] + [maskt] + arrayargs[3:]
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

    pass # end of Zt2Zxy


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


zt2zxy = Zt2Zxy()


# version
__id__ = "$Id$"

# End of file 
