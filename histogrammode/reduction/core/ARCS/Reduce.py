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
            nodes = 8,
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
    # only the master node will carry on
    if mpiRank != 0:
        return
    

    import reduction.interactive as ri
    ri.getRun.select('arcs')

    r = ri.getRun(rundir, instrument_xml = ARCSxml)
    if mtrundir:
        mtr = ri.getRun(mtrundir, instrument_xml = ARCSxml)
    else:
        mtr = None

    idpt = r.getIdpt( tof_params, nodes = nodes )
    if mask: maskbadtubes( mask, idpt.sum('tof'), lowerlimit = criteria_nocounts )
    
    if mtr:
        mtidpt = mtr.getIdpt( tof_params, nodes = nodes )
        if mask: maskbadtubes( mask, mtidpt.sum('tof'), lowerlimit = criteria_nocounts )
        
    from reduction import units
    meV = units.energy.meV

    ri.solveEi.reconstruct( Eaxis = (Ei*0.8*meV, Ei*1.2*meV, 0.005*Ei*meV) )
    calculated_ei = ri.solveEi( run = r, idpt = idpt )
    info.log( 'computed incident energy: %s' % (calculated_ei/meV,) )

    EAxis = H.axis('energy', H.arange(*E_params), 'meV')
    ri.idpt2spe.reconstruct( EAxis = EAxis )
    spe = ri.idpt2spe(calculated_ei, idpt, run = r, mask = mask)
    spe /= r.getIntegratedCurrent()[0]/1.e12, 0
    if mtr:
        mtspe = ri.idpt2spe(calculated_ei, mtidpt, run = mtr, mask = mask)
        mtspe /= mtr.getIntegratedCurrent()[0]/1.e12, 0
        spe -= mtspe * (mtratio,0)
    
    return spe


import histogram as H
from _maskUtils import maskbadtubes


# version
__id__ = "$Id$"

# End of file 
