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
info = journal.info('reduction.core.ARCS.ReduceToMslice')

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
        calibration = mask, mask = mask,
        ARCSxml = ARCSxml,
        E_params = E_params,
        Ei = calculated_ei/meV,
        emission_time = 0,
        )

    if mpiRank !=0 : return

    info.log('I(pdpE) obtained')
    import histogram.hdf as hh
    pdpefile = '%s-IpdpE.h5' % outputprefix
    hh.dump( ipdpE, pdpefile, '/', 'c' )

    info.log('prepare to write mslice files')
    
    from arcseventdata import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    phi_p = infos['phis']
    psi_p = infos['psis']
    
    import numpy
    phi_p.I[:] = numpy.nan_to_num( phi_p.I )
    psi_p.I[:] = numpy.nan_to_num( psi_p.I )

    prefix = outputprefix
    spef = '%s.spe' % prefix
    phxf = '%s.phx' % prefix
    
    #convert to mslice file
    import arcseventdata
    info.log('writing mslice files')
    arcseventdata.write_mslice_files( ipdpE, phi_p, psi_p, spef, phxf )
    return


def reduceToIpdpE(
    rundir,
    mtrundir = None, mtratio = 0.9,
    criteria_nocounts = 10,
    calibration = None, mask = None,
    ARCSxml = 'ARCS.xml',
    E_params = (-60,60,1),
    Ei = 70, emission_time = 0,
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
        eventdatafilename, nevents, ARCSxml, E_params, Ei, emission_time)

    if mpiRank == 0:
        r = ri.getRun(rundir, instrument_xml = ARCSxml)
        ipdpE /= r.getIntegratedCurrent()[0]/1.e12, 0
        info.log('normalizing I(pdpE)')
    
    if mtrundir:
        mteventdatafilename = _eventfile(mtrundir)
        info.log('constructing I(pdpE) for mt run')
        mtnevents = getnumberofevents(mteventdatafilename)
        mtipdpE = toipdpE(
            mteventdatafilename, mtnevents, ARCSxml,
            E_params, Ei, emission_time)

        if mpiRank == 0:
            mtr = ri.getRun(mtrundir, instrument_xml = ARCSxml)
            mtipdpE /= mtr.getIntegratedCurrent()[0]/1.e12, 0
            info.log('normalizing mt I(pdpE)')
            mtipdpE *= mtratio, 0
            info.log('subtracting mt data from main data')
            ipdpE -= mtipdpE

    if mpiRank!=0 : return
    
    if calibration:
        info.log('calibrating')
        calib_pdpE = _fullcalibrationhist(
            calibration, ipdpE.axisFromName('energy' ))
        ipdpE /= calib_pdpE

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
