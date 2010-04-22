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


class IpdpdHistogrammer(base):

    
    def setParameters(
        self,
        ARCSxml, d_params,
        emission_time):
        
        info.log( 'd_params (unit: AA) = %s' % (d_params, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
    
        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        d_begin, d_end, d_step = d_params # angstrom

        d_axis = histogram.axis('d spacing', boundaries = histogram.arange(
                d_begin, d_end, d_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpd)',
            detaxes + [d_axis],
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
        arcseventdata.events2Ipdpd(
            events.ptr, events.n, self.out_histogram, 
            self.pixelPositions,
            mod2sample = self.mod2sample,
            emission_time = self.emission_time,
            )
        return self.out_histogram
        

# version
__id__ = "$Id$"

# End of file 
