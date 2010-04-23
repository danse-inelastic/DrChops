#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import arcseventdata, histogram 


from ParallelHistogrammer import ParallelHistogrammer as base, info


class IqeHistogrammer(base):


    def normalize(self, IQE):
        'normalize IQE'

        # only the master node need to do normalization
        if self.mpiRank != 0: return
        
        #for debug
        from histogram.hdf import dump
        filename = 'IQE-nosolidanglenormalization.h5'
        import os
        if os.path.exists( filename ): os.remove( filename )
        dump( IQE, filename, '/', 'c' )
        
        info.log( 'node %s: convert I(Q,E) datatype from integer to double'
                  % self.mpiRank)
        from histogram import histogram
        newIQE = histogram( IQE.name(), IQE.axes() )
        newIQE[(), ()] = IQE[(), ()]
        
        info.log( 'node %s: normalize I(Q,E) by solid angle' 
                  % self.mpiRank)
        Ei = self.Ei
        pixelPositions = self.pixelPositions
        pixelSolidAngles = self.pixelSolidAngles
        from arcseventdata.normalize_iqe import normalize_iqe
        normalize_iqe( newIQE, Ei, pixelPositions, pixelSolidAngles )
        return newIQE


    def setParameters(
        self,
        Q_params, E_params, ARCSxml, Ei, emission_time):
        
        keys = [
            'detector-system-dimensions',
            'moderator-sample distance',
            'pixelID-position mapping binary file',
            'detector axes',
            'solidangles',
            ]
        infos = self._readInstrumentInfo(ARCSxml, keys=keys)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        self._debug.log( "pixel-positions-filename=%s" % pixelPositionsFilename)
        self._debug.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        self._debug.log( 'Q_params (unit: angstrom^-1) = %s' % (Q_params, ) )
        self._debug.log( 'mod2sample distance = %s' % mod2sample )
        self._debug.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        self._debug.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        E_begin, E_end, E_step = E_params # meV
        Q_begin, Q_end, Q_step = Q_params # angstrom^-1
        
        Q_axis = histogram.axis('Q', boundaries = histogram.arange(
            Q_begin, Q_end, Q_step) )
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        h = histogram.histogram(
            'I(Q,E)',
            [
            Q_axis,
            E_axis,
            ],
            data_type = 'int',
            )

        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet )

        # remember a few things so that we can do normalization
        mpiRank = self.mpiRank
        if mpiRank == 0:
            pixelSolidAngles = infos['solidangles'].I
            self._remember( Ei, pixelPositions, pixelSolidAngles )
            
        self.out_histogram = h
        self.pixelPositions = pixelPositions
        self.Ei = Ei
        self.mod2sample = mod2sample
        self.emission_time = emission_time
        return 


    def _processEvents(self, events):
        h = self.out_histogram
        h = arcseventdata.events2IQE(
            events.ptr, events.n, 
            h, self.Ei, self.pixelPositions,
            mod2sample = self.mod2sample,
            emission_time = self.emission_time,
            )
        return h


    def _remember(self, Ei, pixelPositions, pixelSolidAngles):
        self.Ei = Ei
        self.pixelPositions = pixelPositions
        self.pixelSolidAngles = pixelSolidAngles
        return

    pass # end of Engine


# version
__id__ = "$Id$"

# End of file 
