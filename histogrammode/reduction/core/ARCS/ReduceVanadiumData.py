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


def reduce( vrundir, ARCSxml = 'ARCS.xml', nevents = None,
            E_params = (-60,60,1), Ei = 70, emission_time = 0,
            calibration_returned_withsolidangle = True,
            criteria_nocounts = 10, criteria_toomanycounts = None,
            ):
    '''
    vrundir: directory of vanadium run
    E_params (unit: meV) 
    Ei: Incident energy (unit: meV)
    emission_time (unit: microsecond)
    calibration_returned_withsolidangle: if true, the calibration histogram returned contains solid angle correction. this means the reduction procedure of the dataset to be calibrated need NOT consider solid angle correction.
    criteria_nocounts: if number of counts in a pixel is smaller than this number, the pixel is considered as no-count.
    '''
    # we don't need to compute Ei precisely. The intensity we care
    # is the integrated intensity including elastic and inelastic
    # scatterings bracketed in a range defined by E_params.
    
    runname = os.path.split( vrundir )[-1]
    eventdatafilename = '%s_neutron_event.dat' % runname
    eventdatafilename = os.path.join( vrundir, eventdatafilename )
    
    if not nevents:
        from arcseventdata import getnumberofevents
        nevents = getnumberofevents( eventdatafilename )

    from arcseventdata.parallel_histogrammers.IpdpEHistogrammer import IpdpEHistogrammer
    toipdpE = IpdpEHistogrammer()
    ipdpE = toipdpE( 
        eventdatafilename, nevents,
        ARCSxml, E_params,
        Ei, emission_time)

    # only the master node will carry on
    mpiRank = toipdpE.mpiRank
    if mpiRank != 0:
        return
    
    # I(E)
    iE = ipdpE.sum('detectorpackID').sum('detectorID').sum('pixelID')
    
    # I(pack, tube, pixel)
    ipdp = ipdpE.sum( 'energy' )
    
    # view?
    import arcseventdata as aed
    # view = aed.detectorview( ipdp )
    
    # solid angles
    from reduction.core import ARCS
    sas = ARCS.solid_angles()
    
    # Now correct vanadium data by solid angles
    ipdp_c1 = ipdp.as_floattype()/sas
    
    # Now, Correct for detector efficiency variance among pixels.
    from reduction.core.ARCS import deteff_hist
    from reduction import units 
    deteff = deteff_hist( Ei * units.energy.meV )
        
    # Get a detector view of efficieny
    # deteff_view = aed.detectorview( deteff )
    
    # Correct:
    ipdp_c2= ipdp_c1 / deteff
    # View corrected data
    # view_c2 = aed.detectorview( ipdp_c2 )
    
    # Now average over pixels and we have a good calibration "histogram"
    detaxes = ipdp.axes()
    c = H.histogram( 'calibration', detaxes )
    ipd_c2 = ipdp_c2.sum('pixelID')/(128.,0)
    for pixel in c.pixelID: c[ (), (), pixel ] = ipd_c2
    # calibration_view = aed.detectorview( c )

    # the mask
    mask = newmask( detaxes )
    maskbadtubes( mask, c, lowerlimit = criteria_nocounts, upperlimit = criteria_toomanycounts )
    
    # Reassign tubes with 0 intensity with a large number
    largenumber = c.I.sum() * 1e8
    black = c.I < criteria_nocounts
    c.I[ black ] = largenumber
    
    if calibration_returned_withsolidangle:
        # Put solid angle into this calibration as well. 
        calibration = c * sas
    else:
        calibration = c
        
    # Update the view
    # c_view = aed.detectorview( calibration )
    
    return {
        'calibration': calibration,
        'mask': mask,
        }


import os
import histogram as H
from _maskUtils import newmask, maskbadtubes

# version
__id__ = "$Id$"

# End of file 
