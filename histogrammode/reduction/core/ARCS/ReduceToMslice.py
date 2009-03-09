#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
jrnltag = 'reduction.core.ARCS.ReduceToMslice'
info = journal.info(jrnltag)
debug = journal.debug(jrnltag)

try:
    import mpi
    mpiRank = mpi.world().rank
except ImportError:
    mpiRank = 0


def reduce(
    rundir,
    mtrundir = None, mtratio = 0.9,
    outputprefix = 'mslice',
    criteria_nocounts = 10,
    calibration = None, mask = None,
    ARCSxml = 'ARCS.xml',
    tof_params = (3000,6000,5),
    E_params = (-60,60,1),
    Ei = 70, emission_time = 0,
    pack_params = (1,115),
    pixel_resolution = 1,
    ):
    '''
    rundir: directory of the ARCS run to be reduced
    mtrundir: directory of the empty can run
    mtratio: the ratio of emtpy can data to be subtracted from the main data
    calibration: calibration cosntants as a histogram
    mask: mask as a histogram !!! Not used yet!!!
    E_params (unit: meV) 
    Ei: estimated Incident energy (unit: meV)
    emission_time (unit: microsecond)  !!! NOT used !!!
    '''

    from reduction import units
    info.log('solving Ei. Ei guess = %s' % Ei)
    meV = units.energy.meV
    ri.solveEi.reconstruct( Eaxis = (Ei*0.8*meV, Ei*1.2*meV, 0.005*Ei*meV) )
    ri.getRun.select('arcs')
    r = ri.getRun(rundir, instrument_xml = ARCSxml)
    eventfilename = _eventfile(rundir)
    ipdpt = getIpdpt(eventfilename, ARCSxml, tof_params)

    from arcseventdata.parallel_histogrammers.ParallelComponent import ParallelComponent
    p = ParallelComponent()

    tag = 1000
    if p.mpiRank == 0:
        calculated_ei = ri.solveEi( run = r, idpt = ipdpt )
        info.log('calculated Ei=%s meV' % (calculated_ei/meV,))
        for peer in range(1, p.mpiSize):
            p.mpiSend(calculated_ei, peer=peer, tag=tag)
            continue
    else:
        calculated_ei = p.mpiReceive(peer=0, tag=tag)

    info.log('reducing')
    ipdpE = reduceToIpdpE(
        rundir,
        mtrundir = mtrundir, mtratio = mtratio,
        criteria_nocounts = criteria_nocounts,
        calibration = calibration, mask = mask,
        ARCSxml = ARCSxml,
        E_params = E_params,
        Ei = calculated_ei/meV,
        emission_time = 0,
        pack_params = pack_params,
        pixel_resolution = pixel_resolution,
        )

    if mpiRank !=0 : return

    info.log('I(pdpE) obtained')
    import histogram.hdf as hh
    pdpefile = '%s-IpdpE.h5' % outputprefix
    hh.dump( ipdpE, pdpefile, '/', 'c' )

    write_mslice_files(outputprefix, ipdpE, ARCSxml, pack_params, pixel_resolution)
    return



def write_mslice_files(outputprefix, ipdpE, ARCSxml, pack_params, pixel_resolution):
    info.log('prepare to write mslice files')

    detaxes = ipdpE.axes()[:3]
    phi_p, psi_p, dphi_p, dpsi_p = get_pixel_infos(ARCSxml, detaxes, pack_params, pixel_resolution)
    
    prefix = outputprefix
    spef = '%s.spe' % prefix
    phxf = '%s.phx' % prefix
    
    #convert to mslice file
    import arcseventdata
    info.log('writing mslice files')
    debug.log('shapes=' + str( (ipdpE.shape(), phi_p.shape(), psi_p.shape())) )
    arcseventdata.write_mslice_files( ipdpE, phi_p, psi_p, dphi_p, dpsi_p, spef, phxf )
    return


def get_pixel_infos(ARCSxml, detaxes, pack_params, pixel_resolution):
    # data for resolution=1
    from arcseventdata import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    phi_p1 = infos['phis'][pack_params, (), ()]
    psi_p1 = infos['psis'][pack_params, (), ()]
    dphi_p1 = infos['dphis'][pack_params, (), ()]
    dpsi_p1 = infos['dpsis'][pack_params, (), ()]

    import numpy
    phi_p1.I[:] = numpy.nan_to_num( phi_p1.I )
    psi_p1.I[:] = numpy.nan_to_num( psi_p1.I )

    import histogram as H
    phi_p = H.histogram('phi(pixel)', detaxes)
    psi_p = H.histogram('psi(pixel)', detaxes)

    pixels1 = phi_p1.pixelID
    for pixelID in pixels1:
        phi_p[(), (), pixelID] += phi_p1[(), (), int(pixelID)]
        psi_p[(), (), pixelID] += psi_p1[(), (), int(pixelID)]
        continue
    phi_p /= pixel_resolution,0
    psi_p /= pixel_resolution,0

    # 
    dphi_p = H.histogram('dphi(pixel)', detaxes)
    dpsi_p = H.histogram('dpsi(pixel)', detaxes)
    for pixelID in pixels1:
        dphi_p[(), (), pixelID] += dphi_p1[(), (), int(pixelID)]
        dpsi_p[(), (), pixelID] += dpsi_p1[(), (), int(pixelID)]
        continue
    return phi_p, psi_p, dphi_p, dpsi_p



def mslice_output_filenames( prefix ):
    return [
        '%s.spe'%prefix,
        '%s.phx'%prefix,
        '%s-IpdpE.h5'%prefix,
        ]


def reduceToIpdpE(
    rundir,
    mtrundir = None, mtratio = 0.9,
    criteria_nocounts = 10,
    calibration = None, mask = None,
    ARCSxml = 'ARCS.xml',
    E_params = (-60,60,1),
    Ei = 70, emission_time = 0,
    pack_params = (1,115),
    pixel_resolution = 1,
    ):
    '''
    rundir: directory of the ARCS run to be reduced
    mtrundir: directory of the empty can run
    mtratio: the ratio of emtpy can data to be subtracted from the main data
    calibration: calibration cosntants as a histogram
    mask: mask as a histogram !!! Not used yet!!!
    E_params (unit: meV) 
    Ei: estimated Incident energy (unit: meV)
    emission_time (unit: microsecond)  
    '''
    ri.getRun.select('arcs')
    toipdpE = IpdpEHistogrammer()
    
    eventdatafilename = _eventfile(rundir)
    nevents = getnumberofevents(eventdatafilename)
    info.log('constructing I(pdpE) for main run')
    ipdpE = toipdpE(
        eventdatafilename, nevents, ARCSxml, E_params, pack_params, pixel_resolution, Ei, emission_time)

    if mpiRank == 0:
        ipdpE = ipdpE.as_floattype()
        r = ri.getRun(rundir, instrument_xml = ARCSxml)
        info.log('normalizing I(pdpE)')
        ipdpE /= r.getIntegratedCurrent()[0]/1.e12, 0
        import histogram.hdf as hh
        hh.dump(ipdpE, 'main-ipdpE-normalized.h5', '/', 'c')
    
    if mtrundir:
        mteventdatafilename = _eventfile(mtrundir)
        info.log('constructing I(pdpE) for mt run')
        mtnevents = getnumberofevents(mteventdatafilename)
        mtipdpE = toipdpE(
            mteventdatafilename, mtnevents, ARCSxml,
            E_params, pack_params, pixel_resolution,
            Ei, emission_time)

        if mpiRank == 0:
            mtipdpE = mtipdpE.as_floattype()
            mtr = ri.getRun(mtrundir, instrument_xml = ARCSxml)
            info.log('normalizing mt I(pdpE)')
            mtipdpE /= mtr.getIntegratedCurrent()[0]/1.e12, 0
            mtipdpE *= mtratio, 0
            hh.dump(mtipdpE, 'mt-ipdpE-normalized.h5', '/', 'c')
            info.log('subtracting mt data from main data')
            ipdpE -= mtipdpE
            hh.dump(ipdpE, 'ipdpE-mtsubtracted.h5', '/', 'c')
            # remove negative numbers
            # Is this the right thing to do?
            ipdpE.I[ ipdpE.I<0 ] = 0
            hh.dump(ipdpE, 'ipdpE-mtsubtracted-positive.h5', '/', 'c')

    if mpiRank!=0 : return
    
    if calibration:
        info.log('calibrating')
        # change resolution
        if pixel_resolution != 1:
            calibration = _coarseCalibration(
                calibration, ipdpE.axisFromName('pixelID'), pixel_resolution)
        calib_pdpE = _fullcalibrationhist(
            calibration, ipdpE.axisFromName('energy' ))
        hh.dump( calib_pdpE, 'calibration-full.h5', '/', 'c' )
        ipdpE /= calib_pdpE
        hh.dump( ipdpE, 'ipdpE-calibrated.h5', '/', 'c') 
    info.log('done')
    return ipdpE


def getIpdpt(eventdatafilename, ARCSxml, tof_params):
    toipdpt = IpdptHistogrammer()
    nevents = getnumberofevents(eventdatafilename)
    info.log('constructing I(pdpt) for main run')
    ipdpt = toipdpt(
        eventdatafilename, nevents, ARCSxml, tof_params)
    if mpiRank == 0: return ipdpt.as_floattype()
    return


def _coarseCalibration(calibration, new_pixelID_axis, pixel_resolution,
                       average=False):
    detaxes = calibration.axes()
    newaxes = list(detaxes)
    newaxes[-1] = new_pixelID_axis

    import histogram as H
    new = H.histogram('calibration', newaxes)

    for pixelID in calibration.pixelID:
        new[(), (), pixelID] += calibration[(), (), pixelID]
        continue

    if average:
        new /= (pixel_resolution, 0)

    return new


def _fullcalibrationhist( calibration_pdp, Eaxis ):
    axes = calibration_pdp.axes() + [Eaxis]
    c = H.histogram( 'calibration', axes )
    for E in c.energy: c[ (), (), (), E ] = calibration_pdp
    return c


def _eventfile(rundir):
    import os
    runname = os.path.split( rundir )[-1]
    eventdatafilename = '%s_neutron_event.dat' % runname
    eventdatafilename = os.path.join( rundir, eventdatafilename )
    return eventdatafilename


import histogram as H
from _maskUtils import maskbadtubes
from arcseventdata.parallel_histogrammers.IpdpEHistogrammer import IpdpEHistogrammer
from arcseventdata.parallel_histogrammers.IpdptHistogrammer import IpdptHistogrammer
from arcseventdata import getnumberofevents
import reduction.interactive as ri


# version
__id__ = "$Id$"

# End of file 
