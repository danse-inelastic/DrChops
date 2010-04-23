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


import arcseventdata


from ParallelHistogrammer import ParallelHistogrammer as base, info


class ItofHistogrammer(base):
    
    def setParameters(
        self,
        ARCSxml, tof_params):

        infos = self._readInstrumentInfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        ntotpixels = arcseventdata.npixels( npacks, ndetsperpack, npixelsperdet )
        
        mod2sample = infos['moderator-sample distance']

        info.log( 'tof_params (unit: us) = %s' % (tof_params, ) )

        self.out_histogram = None
        self.ntotpixels = ntotpixels
        self.tof_params = tof_params
        return 


    def _processEvents( self,events):
        h = self.out_histogram
        Itof = arcseventdata.e2Itof(
            events.ptr, events.n, 
            self.ntotpixels,
            tof_params = self.tof_params,
            Itof = h,
            )
        return Itof


# version
__id__ = "$Id$"

# End of file 
