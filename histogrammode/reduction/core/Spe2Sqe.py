#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                            Jiao Lin, Tim Kelley
#
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.Spe2Sqe
## Convert S(phi,E) to S(Q,E)
##
## This component transforms S(phi,E) histogram to S(Q,E) histogram.
## It loops over energy bins, and for each energy  bin, the
## slice S(phi) at the particular energy bin is transformed
## to a S(Q) histogram (the transformation depends on the value
## of E, apparently), and the result is added to the result histogram
## S(Q,E).


import journal
debug = journal.debug( 'reduction.core.Spe2Sqe')
info = journal.info( 'reduction.core.Spe2Sqe')


from histogram import axis, histogram

from ParallelComponent import ParallelComponent

class Spe2Sqe(ParallelComponent):


    """component to convert S(phi,E) to S(Q,E)
    """


    def __call__(self, ei, sphiEHist, QAxis):
        """spe2sqe(ei, sphiEHist, QAxis): convert s(phi,E) histogram to S(Q,E) histogram
        
        ei: incident energy
        sphiEHist: S(phi,E) histogram
        QAxis: Q (momentum transfer) axis
        """
        #trivial parallel (non-parallel)
        channel = 333
        if not self.parallel or self.mpiRank == 0:
            ret = self.__call__1( ei, sphiEHist, QAxis )
            if self.parallel:
                for i in range(1, self.mpiSize):
                    self.mpiSend( ret, i, channel )
                    continue
                pass
            pass
        else:
            ret = self.mpiReceive( 0, channel )
            pass
        return ret


    def __call__1(self, ei, sphiEHist, QAxis):
        """convert s(phi,E) histogram to S(Q,E) histogram

        \arg ei incident energy
        \arg sphiEHist S(phi,E) histogram

        non-parallel version
        """
        unitfactor = self._check_unit( sphiEHist )
        
        EAxis = sphiEHist.axisFromName('energy')
        sQEHist = histogram( 'S(Q,E)', [QAxis, EAxis], unit='1')
        
        # create Q Rebinner
        from reduction.histCompat.QRebinner import QRebinner
        qrebinner = QRebinner( sphiEHist, ei, QAxis)

        qEnergyData = histogram( 'tmpS(Q)', [QAxis], unit = '1' )
        
        info.log("entering -> S(Q,E) loop")

        exfers = EAxis.binCenters()
        
        for exfer in exfers:
            
            # extract phi slice from S(Phi,E)
##             phiData = sphiEHist.extractEnergySlice( exfer, phiDataVector,
##                                                     phiErrorVector)
            phiData = sphiEHist[ (), exfer ]

            # zero temp histogram
            qEnergyData.assign( 0.0)
            
            # feed it to QRebinner
            e_final = ei - exfer * EAxis.unit()
            qrebinner.rebin( phiData, qEnergyData, e_final)
            
            # accumulate the result into correct bin of S( Q, E)
            sQEHist[(), exfer] += qEnergyData

            continue # for loop
            
        info.log("completed S(Q,E) loop")

        #should this unit manipulation implemented in histCompat.QRebinner?
        info.log("**fix units")
        self._fix_sqe_unit( sQEHist, unitfactor )
        
        info.log( "save S(Q,E) using pickle" )
        
        dump( sQEHist, "sqehist.pkl" )
        self._save( sQEHist )
        return sQEHist


    def _check_unit(self, spe):
        #check unit of input hsitogram
        speunit = spe.unit()
        import reduction.units as units
        meV = units.energy.meV
        try:
            speunit + 1./meV
            return speunit*meV
        except:
            try:
                speunit + 1.
                return speunit
            except:
                raise RuntimeError, "S(phi,E) histogram should have a unit of 1/meV or should be unitless"
            raise "Should not reach here"
        raise "should not reach here"


    def _fix_sqe_unit(self, sqe, unitfactor ):
        sqe *= unitfactor, 0
        return


    def _save(self, sQEHist):
        "for backward compatibility, save sqe.hist as numpy arrays"
        import numpy as N
        s = sQEHist.data().storage().asNumarray().copy()
        s.shape = sQEHist.shape()
        s = N.transpose(s).copy()

        serr = sQEHist.errors().storage().asNumarray().copy()
        serr.shape = sQEHist.shape()
        serr = N.transpose(serr).copy()

        q = N.array(sQEHist.axisFromName('Q').binCenters(), copy=1)
        e = N.array(sQEHist.axisFromName('energy').binCenters(), copy=1)

        dump( (q, e, s, serr), 'sqe.pkl')
        return

    pass # end of Spe2Sqe


spe2sqe = Spe2Sqe()

from reduction.utils.hpickle import dump

from pyre.units.energy import meV


# version
__id__ = "$Id$"


# End of file 
