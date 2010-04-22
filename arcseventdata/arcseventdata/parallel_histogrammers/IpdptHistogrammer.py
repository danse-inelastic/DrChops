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

import arcseventdata, histogram


from ParallelHistogrammer import ParallelHistogrammer as base, info

class IpdptHistogrammer(base):

    def setParameters(
        self,
        ARCSxml, tof_params, pack_params = (1,115), pixel_step = 1 ):

        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']

        info.log( 'tof_params (unit: microsecond) = %s' % (tof_params, ) )

        import numpy
        tof_begin, tof_end, tof_step = numpy.array(tof_params)*1.e-6 #convert from microseconds to seconds

        tof_axis = histogram.axis(
            'tof',
            boundaries = histogram.arange(tof_begin, tof_end, tof_step),
            unit = 'second' )
        detaxes = infos['detector axes']

        #pixel axis need to be changed if pixel resolution is not 1
        if pixel_step != 1:
            pixelAxis = detaxes[2]
            npixelspertube = pixelAxis.size()
            pixelAxis = histogram.axis(
                'pixelID',
                boundaries = range(0, npixelspertube+1, pixel_step),
                )
            detaxes[2] = pixelAxis

        #pack axis
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
        self.out_histogram = h
        return 


    def _processEvents( self, events):
        h = self.out_histogram
        arcseventdata.events2Ipdpt(events.ptr, events.n, h )
        return h


# version
__id__ = "$Id$"

# End of file 
