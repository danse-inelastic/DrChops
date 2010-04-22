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

class IpdpEHistogrammer(base):


    def setParameters(
        self, 
        ARCSxml, E_params,
        pack_params, pixel_step,
        Ei, emission_time):

        info.log( 'E_params (unit: meV) = %s' % (E_params, ) )
        info.log( 'Incident energy (unit: meV) = %s' % (Ei, ) )
        info.log( 'emission_time (unit: microsecond) = %s' % (emission_time, ) )

        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        mod2sample = infos['moderator-sample distance']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
    
        E_begin, E_end, E_step = E_params # angstrom

        E_axis = histogram.axis('energy', boundaries = histogram.arange(
            E_begin, E_end, E_step) )

        detaxes = infos['detector axes']
        #pack axis
        startpack, endpack = pack_params
        packaxis = histogram.axis(
            'detectorpackID',
            range( startpack, endpack+1 ) )
        detaxes[0] = packaxis

        #pixel axis need to be changed if pixel resolution is not 1
        if pixel_step != 1:
            pixelAxis = detaxes[2]
            npixelspertube = pixelAxis.size()
            pixelAxis = histogram.axis(
                'pixelID',
                boundaries = range(0, npixelspertube+1, pixel_step),
                )
            detaxes[2] = pixelAxis

        h = histogram.histogram(
            'I(pdpE)',
            detaxes + [E_axis],
            data_type = 'int',
            )
        self.out_histogram = h
        self.Ei = Ei
        self.mod2sample = mod2sample
        self.emission_time = emission_time

        info.log( "reading pixelID->position map..." )
        self.pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)
        
        return
    

    def _processEvents(self, events):
        info.log( "histograming..." )
        arcseventdata.events2IpdpE(
            events.ptr, events.n, self.out_histogram, self.Ei, self.pixelPositions,
            mod2sample = self.mod2sample,
            emission_time = self.emission_time,
            )
        info.log( "done histogramming." )    
        return self.out_histogram


# version
__id__ = "$Id$"

# End of file 
