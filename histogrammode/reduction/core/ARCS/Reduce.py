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
info = journal.info('reduction.core.ARCS.Reduce')

try:
    import mpi
    mpiRank = mpi.world().rank    
except ImportError:
    mpiRank = 0
    

def reduce( rundir,
            mtrundir = None, mtratio = 0.9,
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
    mask: mask as a histogram
    tof_params: define the tof bins to which neutron events are binned 
    E_params (unit: meV) 
    Ei: estimated Incident energy (unit: meV)
    emission_time (unit: microsecond)  !!!!Not used yet!!!!
    '''
    import reduction.interactive as ri
    ri.getRun.select('arcs')

    r = ri.getRun(rundir, instrument_xml = ARCSxml)
    if mtrundir:
        mtr = ri.getRun(mtrundir, instrument_xml = ARCSxml)
    else:
        mtr = None

    idpt = getIpdpt(_eventfile(rundir), ARCSxml, tof_params)
    if mpiRank==0:
        if mask: maskbadtubes(
            mask, idpt.sum('tof'), lowerlimit = criteria_nocounts )
        info.log('normalizing main data...')
        idpt /= r.getIntegratedCurrent()[0]/1.e12, 0
    
    if mtr:
        mtidpt = getIpdpt(_eventfile(mtrundir), ARCSxml, tof_params)
        
        if mpiRank==0:
            if mask: maskbadtubes( mask, mtidpt.sum('tof'), lowerlimit = criteria_nocounts )
            info.log('normalizing mt data...')
            mtidpt /= mtr.getIntegratedCurrent()[0]/1.e12, 0
            mtidpt *= (mtratio, 0)
            info.log('subtracting mt data from main data...')
            idpt -= mtidpt
        
    # only the master node will carry on
    if mpiRank != 0:
        return
    
    if calibration:
        calib_pdpt = _fullcalibrationhist(
            calibration, idpt.axisFromName('tof' ))
        info.log('calibrating...')
        idpt /= calib_pdpt
        
    from reduction import units
    meV = units.energy.meV

    ri.solveEi.reconstruct( Eaxis = (Ei*0.8*meV, Ei*1.2*meV, 0.005*Ei*meV) )
    info.log( 'computing incident energy...' )
    calculated_ei = ri.solveEi( run = r, idpt = idpt )
    info.log( 'computed incident energy: %s' % (calculated_ei/meV,) )

    EAxis = H.axis('energy', H.arange(*E_params), 'meV')
    ri.idpt2spe.reconstruct( EAxis = EAxis )
    info.log( 'reducing...' )

    # !!! don't use parallel version of idpt2spe right now
    ri.idpt2spe._engine.parallel = 0
    # !!!
    spe = ri.idpt2spe(calculated_ei, idpt, run = r, mask = mask)
    info.log( 'done' )
    return spe


def _fullcalibrationhist( calibration_pdp, tofaxis ):
    axes = calibration_pdp.axes() + [tofaxis]
    c = H.histogram( 'calibration', axes )
    for tof in c.tof: c[ (), (), (), tof ] = calibration_pdp
    return c


def _eventfile(rundir):
    import os
    runname = os.path.split( rundir )[-1]
    eventdatafilename = '%s_neutron_event.dat' % runname
    eventdatafilename = os.path.join( rundir, eventdatafilename )
    return eventdatafilename


def getIpdpt(eventdatafilename, ARCSxml, tof_params):
    from arcseventdata.parallel_histogrammers.IpdptHistogrammer import IpdptHistogrammer
    toipdpt = IpdptHistogrammer()
    from arcseventdata import getnumberofevents
    nevents = getnumberofevents(eventdatafilename)
    info.log('constructing I(pdpt) for main run')
    ipdpt = toipdpt(
        eventdatafilename, nevents, ARCSxml, tof_params)
    if mpiRank == 0: return ipdpt.as_floattype()
    return


import histogram as H
from _maskUtils import maskbadtubes


# version
__id__ = "$Id$"

# End of file 
