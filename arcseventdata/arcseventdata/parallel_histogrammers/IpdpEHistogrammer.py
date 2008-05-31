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

class IpdpEHistogrammer(base):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, E_params,
              Ei, emission_time):
        
        info.log( "eventdatafilename = %s" % eventdatafilename )
        info.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        info.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )
        info.log( 'neutrons: start = %d, n = %d' % (
            start, nevents ) )
    
        from arcseventdata.getinstrumentinfo import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        E_begin, E_end, E_step = E_params # angstrom

        import arcseventdata, histogram 
        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )
        detaxes = infos['detector axes']
        h = histogram.histogram(
            'I(pdpE)',
            detaxes + [E_axis],
            data_type = 'int',
            )

        info.log( "reading %d events..." % nevents )
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
        info.log( "reading pixelID->position map..." )
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)

        info.log( "histograming..." )
        arcseventdata.events2IpdpE(
            events, nevents, h, Ei, pixelPositions,
            mod2sample = mod2sample,
            emission_time = emission_time,
            )

        info.log( "done histogramming." )
    
        return h


# version
__id__ = "$Id$"

# End of file 
