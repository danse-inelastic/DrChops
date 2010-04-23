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


class IpdpLHistogrammer(base):

    def setParameters(
        self,
        ARCSxml, L_params,
        emission_time):
        
        info.log( 'L_params (unit: AA) = %s' % (L_params, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        infos = self._readInstrumentInfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        L_begin, L_end, L_step = L_params # meV

        L_axis = histogram.axis('L', boundaries = histogram.arange(
            L_begin, L_end, L_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpL)',
            detaxes + [L_axis],
            data_type = 'int',
            )

        info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        self.out_histogram = h
        self.pixelPositions = pixelPositions
        self.mod2sample = mod2sample
        self.emission_time = emission_time
        return


    def _processEvents( self, events):
        h = self.out_histogram
        arcseventdata.events2IpdpL(
            events.ptr, events.n, h, 
            self.pixelPositions,
            mod2sample = self.mod2sample,
            emission_time = self.emission_time,
            )
        return h



# version
__id__ = "$Id$"

# End of file 
