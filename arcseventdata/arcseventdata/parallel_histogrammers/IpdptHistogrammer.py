# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from ParallelHistogrammer import ParallelHistogrammer as base, info

class IpdptHistogrammer(base):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, tof_params, pack_params = (1,115) ):

        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']

        info.log( "eventdatafilename = %s" % eventdatafilename )
        info.log( "nevents = %s" % nevents )
        info.log( 'tof_params (unit: microsecond) = %s' % (tof_params, ) )

        import numpy
        tof_begin, tof_end, tof_step = numpy.array(tof_params)*1.e-6 #convert from microseconds to seconds

        import arcseventdata, histogram 
        tof_axis = histogram.axis(
            'tof',
            boundaries = histogram.arange(tof_begin, tof_end, tof_step),
            unit = 'second' )
        detaxes = infos['detector axes']

        #pack axis needs attention
        startpack, endpack = pack_params
        packaxis = histogram.axis(
            'detectorpackID',
            range( startpack, endpack+1 ) )
        detaxes[0] = packaxis
        
        h = histogram.histogram(
            'I(pdpt)',
            detaxes + [tof_axis],
            data_type = 'int',
            )

        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )

        arcseventdata.events2Ipdpt(
            events, nevents, h )
        
        return h


# version
__id__ = "$Id$"

# End of file 
