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


class IpdpEiHistogrammer(base):


    def setParameters(
        self,
        ARCSxml, Ei_params,
        emission_time):
        
        info.log( 'Ei_params (unit: meV) = %s' % (Ei_params, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )

        infos = self._readInstrumentInfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        Ei_begin, Ei_end, Ei_step = Ei_params # meV

        Ei_axis = histogram.axis('Ei', boundaries = histogram.arange(
            Ei_begin, Ei_end, Ei_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpI)',
            detaxes + [Ei_axis],
            data_type = 'int',
            )

        info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        self.pixelPositions = pixelPositions
        self.mod2sample = mod2sample
        self.emission_time = emission_time
        self.out_histogram = h
        return 


    def _processEvents( self, events):
        h = self.out_histogram
        arcseventdata.events2IpdpEi(
            events.ptr, events.n, h, 
            self.pixelPositions,
            mod2sample = self.mod2sample,
            emission_time = self.emission_time,
            )
        return h



# version
__id__ = "$Id$"

# End of file 
