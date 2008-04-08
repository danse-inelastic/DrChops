#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2005 All Rights Reserved  
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.pyre.TrivialIncidentEnergySolver
## An implementation of IncidentEnergySolver that retrieves Ei directly from user input


from AbstractIncidentEnergySolver import AbstractIncidentEnergySolver as base



class TrivialIncidentEnergySolver(base):

    """ Simple incident energy solver

    This solver is not really a solver. User simply guess the incident
    energy and input it here.
    
    The ARCS incident enery solver is based on fitting peaks in the
    beam monitor spectra to determine the TOF along a known distance,
    and then converting that time to an energy. Pharos does not seem
    to be using monitors at present. To determine energy, they fit the
    time at which the elastic peak arrives in the detectors.
    
    To create a component that determines E_i for Pharos, one will need
    to do something similar to what the existing IncidentEnergySolver
    does, but working on the detector data. You have several choices for
    how to do that. For instance, the Pharos file stores C( det#, tof)
    in a dataset called psd_tof,
    and may even have just C( tof); you could probably fit either
    detector by detector or just sum over all detectors and do one fit.
    To see how to read in that data, look at getVanadiumData in
    PharosMeasurement--it's the same data set, only you're looking for
    the one in the data file, not the one in the calibration file.
    
    In the meantime, I'll hard code E_i, but leave the logic for calling
    the E_i solver in place.
    """
    
    class Inventory(base.Inventory):
        import pyre
        e_i = pyre.inventory.float('e_i', default = 75 )
        e_i.meta['tip'] = 'set this one to the neutron incidenet energy'
        pass
    
    def __call__(self, *args, **kwds): return self.e_i

    def __init__(self,name = "TrivialIncidentEnergySolver"):
        base.__init__(self, name)
        return

    def _configure(self):
        base._configure(self)
        self.e_i = self.inventory.e_i
        return
    
    pass



# version
__id__ = "$Id: TrivialIncidentEnergySolver.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
