#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.Idpt2Spe_a
## An implemenation of AbstractIdpt2Spe.
## The algorithm is to go thru each pixel and convert I(tof)
## to I(E) and add them to appropriate phi-slice of the result
## histogram I(phi,E).
##
##   1. there is a loop that loops over all detector and pixels
##      and for each pixel its scattering angle and distance-to-sample
##      is recorded in a data object (currently "histogram")
##   2. there is another step that converts I(det,pix,tof) to
##      I(phi,E) using the data objects obtained in step 1.
##
## Step 1 is implemented in class DataCollector
##
## Step 2 currently has two implementation classes:
##   - IteratorRebinner
##   - StdVectorRebinner
##
## StdVectorRebinner is an implementation that is mostly inherited
## Tim's code. The loop is implemented in python so it is slower.
##
## IteratorRebinner is an implementation that is basically
## one call to the c++ rebinner. The c++ rebinner uses iterators
## as inputs so it is quite flexible. Because it is implented
## in c++, it is also quite fast.
##
##



import journal
jname = "reduction.core.Idpt2Spe_a"
debug = journal.debug( jname )
info = journal.info( jname )
warning = journal.warning( jname )


from ParallelComponent import ParallelComponent

from AbstractIdpt2Spe import AbstractIdpt2Spe
class Idpt2Spe_a(ParallelComponent, AbstractIdpt2Spe):

    """ reduce I(det, pix, tof) to S(phi,E) histogram

    This reducer goes through each pixel and convert I(tof)
    spectrum of that pixel to I(E) spectrum, and then add
    the I(E) spectrum to the slice of result S(phi,E)
    histogram where phi = phi(pixel).
    """

    parameters = {
        'rebinner': 'rebinner',
        'phiAxis': "phi axis. instance of histogram.Axis",
        'EAxis': 'energy axis. instance of histogram.Axis',
        'mask': "detector mask",
        }
    parameterDocs = '\n  Parameters:\n' 
    parameterDocs += '\n'.join (
        [ "    %s: %s" % (k,v) for k,v in parameters.iteritems() ])
    

    def __init__(self, name = "Idpt2Spe_a", **kwds):
        '''__init__( name='Idpt2Spe_a', **params ) --> new I(d,p,t)->S(phi,E) reducer'''
        import journal

        self.setDefaults( )
        self.set(**kwds)
        return
    __init__.__doc__ += parameterDocs


    def __call__(self, ei, Idpt, instrument, geometer, mask_dp = None,
                 **params):
        '''__call__(ei, Idpt, instrument, geometer, **params)
  Inputs:
    ei: incident energy
    Idpt: I(det, pix, tof) histogram
    instrument: instrument hierarchy
    geometer: geometry information holder
    '''
        
        self.set( **params )
        
        sphiEHist, solidAngleHist = self.reduce_(
            ei, Idpt, instrument, geometer, mask_dp = mask_dp)

        if self.parallel:

            #debug
            #dump( sphiEHist, open( 'spehist%s.pkl' % self.mpiRank, 'w' ) )
        
            channel = 999
            
            if self.mpiRank !=0:
                self.mpiSend( (sphiEHist, solidAngleHist), 0, channel )
            else:
                for i in range( 1, self.mpiSize ):
                    spe, sa = self.mpiReceive( i, channel )
                    sphiEHist += spe
                    solidAngleHist += sa
                    continue
                pass

            pass # end if self.parallel

        channel = 1000
        # if not main node, get result from main node
        if self.parallel and self.mpiRank != 0:
            ret = self.mpiReceive( 0, channel )
            return ret
        
        # temp hack
        self._writeSpe( sphiEHist, "spe-nonormalization.pkl" )
        
        info.log( "normalize S(phi,E) by solid angle" )

        # make sure solid angle histogram does not contain 0.0
        self._checkSolidAngleHist( solidAngleHist )

        #normalize
        for e in sphiEHist.axisFromName('energy').binCenters():
            slice = sphiEHist[(),e].copy()
            slice /= solidAngleHist
            sphiEHist[(),e] = slice
            continue
        
        info.log("S( phi, E) loop completed")
        
        #write data to a file
        self._writeSpe( sphiEHist )

        #now we are done
        #send result to other nodes if necessary
        if self.parallel and self.mpiRank == 0:
            for i in range(1, self.mpiSize):
                self.mpiSend( sphiEHist, i, channel )
                continue
            pass
            
        return sphiEHist
    __call__.__doc__ += parameterDocs



    # implementation details
    
    def reduce_(self, ei, Idpt, instrument, geometer, mask_dp = None):

        info.log("create hisotgrams to hold results")
        from histogram import histogram
        spe = histogram( "SphiE", (self.phiAxis, self.EAxis), unit = "1/meV" )
        sap = histogram( 'solid angle', (self.phiAxis,) )

        info.log("start gathering data for reduction")
        detaxes = Idpt.axes()[:-2] # usually we take all pixels
        phi_dp, sa_dp, dist_dp, radius_dp, pressure_dp = getPixelGeometricInfo(
            instrument, geometer, detaxes )
        
        mod2SampleDist = geometer.distanceToSample( instrument.getModerator() )

        rebinner = self.rebinner

        info.log("reduce I(det,pix,tof) to I(phi,E) and solidangle(phi)")

        # for debug, save all data
        #import pickle
        #pickle.dump( (ei, mod2SampleDist, self.mask, phi_dp, sa_dp, dist_dp,
        #              radius_dp, pressure_dp), open('tobereduced.pkl','w') )
        rebinner(Idpt, spe, sap, ei, mod2SampleDist,
                 self.mask, phi_dp, sa_dp, dist_dp, radius_dp, pressure_dp,
                 mask_dp = mask_dp)

        return spe, sap


    def setDefaults(self):

        self.rebinner = IteratorRebinner()

        from instrument.DetectorMask import DetectorMask
        self.mask = DetectorMask()

        from histogram import axis, arange
        self.EAxis = axis('energy', arange(-45, 45, 1.), unit='meV')
        #be careful with phi axis. all bin boundaries must be larger than zero
        self.phiAxis = axis('phi', boundaries = arange(0.0, 101.0, 1.0), unit='degree')

        return


    def set(self, **params):
        for k, v in params.iteritems():
            if k not in self.parameters.iterkeys():
                raise "Cannot set parameter %s to %s: unknown" % (
                    k,v )
            self.__dict__[ k ] = v
            continue
        return


    def _checkSolidAngleHist(self, solidAngleHist):
        a = solidAngleHist.data().storage().asNumarray()
        ave = a.sum()/a.size
        a += ave * 1.e-10
        return


    def _sphiE2tuple( self, sphiEHist ):
        import numpy as N
        phi = sphiEHist.axisFromName('phi').binCenters()
        e = sphiEHist.axisFromName('energy').binCenters()
        
        spe = sphiEHist.data().storage().asNumarray().copy()
        spe.shape = len(phi), len(e)
        spe = N.transpose( spe ).copy()
        
        speerrs = sphiEHist.errors().storage().asNumarray().copy()
        speerrs.shape = len(phi), len(e)
        speerrs = N.transpose( speerrs ).copy()
        return phi, e, spe, speerrs


    def _writeSpe( self, sphiEHist, filename = "spe.pkl"):
        #that is an ugly implementation
        phi, e, spe, speerrs = self._sphiE2tuple( sphiEHist )
        dump( (phi, e, spe, speerrs), filename )
        
        dump( sphiEHist, filename.replace(".pkl", "hist.pkl" ) )
        return


    pass # end of Idpt2Spe_a


from reduction.utils.hpickle import dump


# helpers
def _create_spe( phiAxis, EAxis ):
    "create an zerod histogram with axes phi and E"
    phiEHist = histogram(
        "SphiE", (phiAxis, EAxis), unit = "1/meV" )
    return phiEHist



from getPixelInfo import getPixelGeometricInfo


class IteratorRebinner:

    ''' this rebinner does not correct for detector efficiency

    This rebinner uses c++ rebinner based on iterators.
    '''
    def __call__( self, Idpt, spe, sap, ei, mod2sample,
                  mask, phi_dp, sa_dp, dist_dp,
                  radius_dp, pressure_dp, mask_dp = None):

        from histogram import histogram
        detaxes = phi_dp.axes()

        if mask_dp is None:
            mask_dp = histogram( 'mask', detaxes, data_type = 'int')
            self._make_mask_dp( mask_dp, mask )

        from reduction.histCompat.DGTS_RebinTof2E_batch import dgts_RebinTof2E_batch

        #print Idpt, spe, sap, ei, mod2sample, mask_dp, phi_dp, sa_dp, dist_dp
        dgts_RebinTof2E_batch(
            Idpt, spe, sap,
            ei, mod2sample, 
            mask_dp, phi_dp, sa_dp, dist_dp,
            radius_dp, pressure_dp)

##         from histogram.plotter import defaultPlotter
##         defaultPlotter.plot( spe )
##         raw_input( 'Press <ENTER> to continue' )
        return


    def _make_mask_dp(self, mask_dp, mask):
        'make a mask(detectorindexes) histogram from a mask instance'
        
        detaxis = mask_dp.axisFromName( 'detectorID' )
        pixaxis = mask_dp.axisFromName( 'pixelID' )
        
        dets = detaxis.binCenters()
        pixs = pixaxis.binCenters()
        
        for det in mask.excludedDetectors:
            if det not in dets: continue
            mask_dp[ {'detectorID':det} ] = 1,0
            continue
        for pix in mask.excludedPixels:
            if pix not in pixs: continue
            mask_dp [ {'pixelID': pix} ] = 1,0
            continue
        for det,pix in mask.excludedSingles:
            if det not in dets: continue
            if pix not in pixs: continue
            mask_dp [ { 'detectorID':det, 'pixelID':pix} ] = 1, 0
            continue

        return
    
    pass # end of IteratorRebinner



# version
__id__ = "$Id: Idpt2Spe_a.py 1254 2007-05-03 18:45:19Z linjiao $"

# End of file 
