#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


def detectorview( pdphist ):
    '''create a 2d view of ARCS detectors given a histogram.
    The first 3 axes of given histogram must be pack, tube, pixel.
    '''
    from detectorview_hist import detectorview
    return detectorview( pdphist )



def getnumberofevents( eventdatafilename ):
    import journal, os
    info = journal.info('getnumberofevents')
    info.log( "eventdatafilename = %s" % eventdatafilename )
    nbytes = os.path.getsize( eventdatafilename )
    nevents = nbytes/8
    info.log( "number of bytes = %s" % nbytes )
    info.log( "number of events = %s" % nevents )
    return nevents


def getinstrumentinfo( *args, **kwds ):
    from _getinstrumentinfo import getinstrumentinfo
    return getinstrumentinfo( *args, **kwds )


def readevents( filename, n, start = 0):
    ntotal = getnumberofevents( filename )
    if start >= ntotal : raise IOError, "no neutrons to read"
    if start+n > ntotal: n = ntotal - start
    events = binding.readevents( filename, n, start )
    return events, n


def readpixelpositions( filename,
                        npacks = 115, ndetsperpack = 8, npixelsperdet = 128):
    s = open(filename).read()
    import numpy
    arr = numpy.fromstring( s, numpy.double )
    arr.shape = -1,3
    checkpixelpositions( arr, npacks, ndetsperpack, npixelsperdet )
    return arr


def npixels( npacks, ndetsperpack, npixelsperdet ):
    '''return number of "pixels". this is actually the maximum longpixelID + 1
    see longpixelID.py for more details.
    '''
    from longpixelID import PixelIDMapper
    m = PixelIDMapper( npixelsperdet, ndetsperpack, npacks )
    return m.ntotpixels


def checkpixelpositions( pixelpositions, npacks, ndetsperpack, npixelsperdet ):
    assert npixels(npacks, ndetsperpack, npixelsperdet) == len( pixelpositions )
    return


def e2Id(
    events, n, pixelpositions, 
    dspacing_params = None,
    Idspacing = None,
    preNeXus_tofUnit = 1.e-7, mod2sample = 13.5):
    '''e2Id(events, n, pixelpositions, Idspacing = None,
    dspacing_params = None,
    npacks = 115, ndetsperpack = 8, npixelsperdet = 128,
    preNeXus_tofUnit = 1.e-7, mod2sample = 13.5) --> integrate events to I(d spacing) histogram

    Either Idspacing or dspacing_params must be given

    Idspacing:
      histogram I(d spacing). If this is None, a histogram will be created
      using dspacing_params.
    dspacing_params:
      begin, end, and step of dspacing. unit: angstrom
      If Idspacing is given, this is ignored.
    events:
      neutron events
    n:
      number of neutron events to process
    pixelpositions:
      array of pixel positions
    preNeXus_tofUnit:
      unit of event.tof in the pre-Nexus data format. unit: second
    mod2sample:
      moderator-sample distance. unit: meter

    return:
      the I(d spacing) histogram
    '''
    

    if Idspacing is None:
        if dspacing_params is None:
            raise ValueError, "Must provide either the (min, max, step) of d axis or the I(d) histogram"
        dspacing_begin, dspacing_end, dspacing_step = dspacing_params # angstrom
        
        import histogram 
        daxis = histogram.axis(
            'd',
            boundaries = histogram.arange(dspacing_begin, dspacing_end, dspacing_step),
            unit = 'angstrom',
            )
        
        Idspacing = histogram.histogram(
            'I(d spacing)',
            [daxis],
            data_type = 'int',
            )

        pass

    events2Idspacing(
        events, n, Idspacing, pixelpositions,
        tofUnit = preNeXus_tofUnit, mod2sample = mod2sample)

    return Idspacing



def e2Itof(
    events, nevents, ntotpixels,
    tof_params = None, Itof = None, 
    preNeXus_tofUnit = 1.e-7):
    '''e2Itof(events, nevents, 
    tof_params = None, Itof = None,
    preNeXus_tofUnit = 1.e-7) --> integrate events into I(tof) histogram

    Either tof_params or Itof must be given
    
    events:
      neutron events
    nevents:
      number of events
    Itof:
      I(tof) histogram. If this is None, a histogram will be created using
      tof_params.
    tof_params:
      min, max, and step of tof axis. unit is microseconds
      If Itof is given, this is ignored.
    preNeXus_tofUnit:
      tof unit in the pre_Nexus file
    '''

    if Itof is None:

        tof_begin, tof_end, tof_step = tof_params

        import histogram 
        tof_axis = histogram.axis(
            'tof',
            boundaries = histogram.arange(tof_begin, tof_end, tof_step),
            unit = 'microsecond')
    
        Itof = histogram.histogram(
            'I(tof)',
            [
            tof_axis,
            ],
            data_type = 'int',
            )
        pass
    
    events2Itof(
        events, nevents, ntotpixels,
        Itof,
        tofUnit = preNeXus_tofUnit)
    
    return Itof



#from pixelpositions2angles import pixelpositions2angles

def write_mslice_files( IpE, phi_p, psi_p, spefile, phxfile ):
    from mslice_spe_writer import writer
    writer.write_spe( IpE, phi_p, spefile )
    writer.write_phx( phi_p, psi_p, phxfile )
    return



from events2Idspacing import events2Idspacing
from events2IpdpE import events2IpdpE
from events2Ipdpd import events2Ipdpd
from events2IQE import events2IQE
from events2IQQQE import events2IQQQE
from events2Ipdpt import events2Ipdpt
from events2Itof import events2Itof


import arcseventdata as binding



# version
__id__ = "$Id$"

#  End of file 
