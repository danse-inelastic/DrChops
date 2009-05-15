#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.vectorCompat.QRebinner
## rebin data in phi bins to Q bins

from reduction import reduction as red
from stdVector import vector

class QRebinner( object):

    import journal
    _info = journal.info('rebin')
    _debug = journal.debug('rebin')

    def __call__( self, e_final, indata, outdata, inerrs, outerrs):
        """my_QRebinDriver( e_final, indata, outdata, inerrs, outerrs)
        Rebin some data from S(Phi, e_final) to S(Q, e_final).
        Inputs:
            e_final( float, final neutron energy in meV)
            indata (StdVector, input data, unchanged)
            outdata (StdVector, output data, CHANGED)
            inerrs (StdVector, input errors squared, unchanged)
            outerrs (StdVector, output errors squared, CHANGED)
        Output: None
        Exceptions: TypeError
        """
        self._qbincalc( e_final, self._qbbo)

        indata = indata.as_(vectorType)
        inerrs = inerrs.as_(vectorType)
        red.ERebinAllInOne_call( self._rebinner._templateType, self._rebinner._handle,
                                 self._qbbo._handle, self._qbbn._handle,
                                 indata._handle, inerrs._handle,
                                 outdata._handle, outerrs._handle)
        return
        

    def __init__( self, phiBB, dphi, ei, qbbn, phiInRadians=False,
                  mod2SampDist = 13600.0):
        """QRebinDriver( phiBB, delta_phi, ei, qBB, phiInRadians=True) ->
        new QRebinDriver
        Create an object that knows how to rebin from phi to Q.
        Inputs:
            phiBB (StdVector, constant phi bin bounds, in degrees or radians)
            dphi (float, phi bin spacing)
            ei (float, fixed energy in meV)
            qbbn (StdVector, constant Q bin boundaries, in inverse Angstroms)
            phiInRadians (boolean, are the angles in phiBB in radians? Default
                is False)
        Output:
            new instance of QRebinDriver
        Exceptions: ValueError
        """
        self._dphi = dphi
        self._phiBB = phiBB
        self._ei = ei
        self._qbbn = qbbn

        # storage for phi bin boundaries expressed as q:
        self._qbbo = vector( self._phiBB.datatype(), self._phiBB.size())

        # Create q bin calculator (computes old q-bins given E_f)
        from QBinCalcor import QBinCalc
        self._qbincalc = QBinCalc( phiBB, ei, phiInRadians)

        # create ERebinAllInOne. It will be used, with de = dt = 1.0, to do
        # rebinning. Aside from the Jacobian, there is nothing time/energy
        # specific about it. We could simply go to the module, and skip the
        # python version...
        from ERebinAllInOne import ERebinAllInOne
        self._rebinner = ERebinAllInOne( phiBB.datatype(), phiBB.size() - 1,
                                         qbbn.size() - 1, ei, mod2SampDist,
                                         1.0, 1.0)
        return


vectorType = "StdVectorNdArray"


# version
__id__ = "$Id: QRebinner.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
