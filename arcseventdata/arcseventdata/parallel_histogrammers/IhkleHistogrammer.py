#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ParallelHistogrammer import ParallelHistogrammer as base, info


class IhkleHistogrammer(base):


    def normalize(self, IhklE):
        'normalize IhklE'

        # only the master node need to do normalization
        if self.mpiRank != 0: return
        
        #for debug
        #from histogram.hdf import dump
        #filename = 'IhklE-nosolidanglenormalization.h5'
        #import os
        #if os.path.exists( filename ): os.remove( filename )
        #dump( IhklE, filename, '/', 'c' )
        
        info.log( 'node %s: normalize I(vector Q,E) by solid angle' 
                  % self.mpiRank)
        Ei = self.Ei
        ub = self.ub
        pixelPositions = self.pixelPositions
        from arcseventdata.normalize_ihkle import normalize_ihkle
        normalize_ihkle( IhklE, Ei, ub, pixelPositions )
        return IhklE
    

    def _run( self,
              eventdatafilename, start, nevents,
              h_params, k_params, l_params,
              E_params, ARCSxml, Ei, ub, emission_time):
        
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
        self._debug.log( 'h_params = %s' % (h_params, ) )
        self._debug.log( 'k_params = %s' % (k_params, ) )
        self._debug.log( 'l_params = %s' % (l_params, ) )
        self._debug.log( 'mod2sample distance = %s' % mod2sample )
        self._debug.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        self._debug.log( 'Matrix: Q->hkl = %s' % (ub, ) )
        self._debug.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        E_begin, E_end, E_step = E_params # meV
        h_begin, h_end, h_step = h_params 
        k_begin, k_end, k_step = k_params 
        l_begin, l_end, l_step = l_params 
        
        import arcseventdata, histogram 
        h_axis = histogram.axis('h', boundaries = histogram.arange(
            h_begin, h_end, h_step))
        k_axis = histogram.axis('k', boundaries = histogram.arange(
            k_begin, k_end, k_step))
        l_axis = histogram.axis('l', boundaries = histogram.arange(
            l_begin, l_end, l_step))
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        h = histogram.histogram(
            'I(h,k,l,E)',
            [
            h_axis,
            k_axis,
            l_axis,
            E_axis,
            ],
            data_type = 'double',
            )

        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet )

        # remember a few things so that we can do normalization
        mpiRank = self.mpiRank
        if mpiRank == 0: self._remember( Ei, ub, pixelPositions )
        
        h = arcseventdata.events2IhklE(
            events, nevents, h, Ei, ub, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )
    
        return h


    def _remember(self, Ei, ub, pixelPositions):
        self.Ei = Ei
        self.ub = ub
        self.pixelPositions = pixelPositions
        return

    pass # end of Engine


# version
__id__ = "$Id$"

# End of file 
