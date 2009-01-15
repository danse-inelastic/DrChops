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


class IpdpdHistogrammer(base):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, d_params,
              emission_time):
        
        info.log( "eventdatafilename = %s" % eventdatafilename )
        info.log( 'd_params (unit: AA) = %s' % (d_params, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
        info.log( 'neutrons: start = %d, n = %d' % (
            start, nevents ) )
    
        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        d_begin, d_end, d_step = d_params # angstrom

        import arcseventdata, histogram 
        d_axis = histogram.axis('d spacing', boundaries = histogram.arange(
            d_begin, d_end, d_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpd)',
            detaxes + [d_axis],
            data_type = 'int',
            )

        info.log( "reading %d events..." % nevents )
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        info.log( "histograming..." )
        arcseventdata.events2Ipdpd(
            events, nevents, h, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )

        info.log( "done histogramming." )
    
        return h



# version
__id__ = "$Id$"

# End of file 