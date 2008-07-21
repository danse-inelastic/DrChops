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


from ParallelHistogrammer import ParallelHistogrammer as base, info


class IqqqeHistogrammer(base):


    def normalize(self, IQQQE):
        'normalize IQQQE'

        # only the master node need to do normalization
        if self.mpiRank != 0: return
        
        #for debug
        #from histogram.hdf import dump
        #filename = 'IQQQE-nosolidanglenormalization.h5'
        #import os
        #if os.path.exists( filename ): os.remove( filename )
        #dump( IQQQE, filename, '/', 'c' )
        
        info.log( 'node %s: normalize I(vector Q,E) by solid angle' 
                  % self.mpiRank)
        Ei = self.Ei
        pixelPositions = self.pixelPositions
        from arcseventdata.normalize_iqqqe import normalize_iqqqe
        normalize_iqqqe( IQQQE, Ei, pixelPositions )
        return IQQQE
    

    def _run( self,
              eventdatafilename, start, nevents,
              Qx_params, Qy_params, Qz_params,
              E_params, ARCSxml, Ei, emission_time):
        
        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']

        self._debug.log( "eventdatafilename = %s" % eventdatafilename)
        self._debug.log( "nevents = %s" % nevents)
        self._debug.log( "pixel-positions-filename=%s" % pixelPositionsFilename)
        self._debug.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        self._debug.log( 'Qx_params (unit: angstrom^-1) = %s' % (Qx_params, ) )
        self._debug.log( 'Qy_params (unit: angstrom^-1) = %s' % (Qy_params, ) )
        self._debug.log( 'Qz_params (unit: angstrom^-1) = %s' % (Qz_params, ) )
        self._debug.log( 'mod2sample distance = %s' % mod2sample )
        self._debug.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        self._debug.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        E_begin, E_end, E_step = E_params # meV
        Qx_begin, Qx_end, Qx_step = Qx_params 
        Qy_begin, Qy_end, Qy_step = Qy_params 
        Qz_begin, Qz_end, Qz_step = Qz_params 
        
        import arcseventdata, histogram 
        Qx_axis = histogram.axis('Qx', boundaries = histogram.arange(
            Qx_begin, Qx_end, Qx_step), unit = 'angstrom**-1' )
        Qy_axis = histogram.axis('Qy', boundaries = histogram.arange(
            Qy_begin, Qy_end, Qy_step), unit = 'angstrom**-1' )
        Qz_axis = histogram.axis('Qz', boundaries = histogram.arange(
            Qz_begin, Qz_end, Qz_step), unit = 'angstrom**-1' )
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        h = histogram.histogram(
            'I(Qx,Qy,Qz,E)',
            [
            Qx_axis,
            Qy_axis,
            Qz_axis,
            E_axis,
            ],
            data_type = 'double',
            )

        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet )

        # remember a few things so that we can do normalization
        mpiRank = self.mpiRank
        if mpiRank == 0: self._remember( Ei, pixelPositions )
        
        h = arcseventdata.events2IQQQE(
            events, nevents, h, Ei, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )
    
        return h


    def _remember(self, Ei, pixelPositions):
        self.Ei = Ei
        self.pixelPositions = pixelPositions
        return

    pass # end of Engine


# version
__id__ = "$Id$"

# End of file 
