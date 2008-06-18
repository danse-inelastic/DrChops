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


class ItofHistogrammer(base):

    def _run( self,
              eventdatafilename, start, nevents,
              ARCSxml, tof_params):

        from arcseventdata import getinstrumentinfo
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        import arcseventdata
        ntotpixels = arcseventdata.npixels( npacks, ndetsperpack, npixelsperdet )
        
        mod2sample = infos['moderator-sample distance']

        info.log( "eventdatafilename = %s" % eventdatafilename )
        info.log( "nevents = %s" % nevents )
        info.log( 'tof_params (unit: us) = %s' % (tof_params, ) )
        
        events, nevents = arcseventdata.readevents( eventdatafilename, nevents, start )
    
        tof_begin, tof_end, tof_step = tof_params

        h = arcseventdata.e2Itof(
            events, nevents, ntotpixels,
            tof_params = tof_params)
        
        return h


# version
__id__ = "$Id$"

# End of file 
