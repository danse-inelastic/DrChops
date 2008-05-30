#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.pyre.IncidentEnergySolver_UseElasticPeaks
## Use monitor data to calculate incident neutron energy



def verifyDetectorSlice( candidate ):
    try:
        t = eval( candidate )
    except:
        raise ValueError, "%s is not even evaluable" % (candidate,)
    assert isinstance(t, tuple)
    for s in t:
        assert isinstance(s, tuple) and len(s) in [0,2]
        if len(s) == 0: continue
        begin, end = s
        assert isinstance( begin, int )
        assert isinstance( end, int )
        continue
    return candidate


from AbstractIncidentEnergySolver import AbstractIncidentEnergySolver as base


class IncidentEnergySolver_UseElasticPeaks(base):
    
    """
    An implementation of EiSolver that calcualte Ei from data of two monitors.
    """

    class Inventory(base.Inventory):

        import pyre.inventory as inv

        numPoints = inv.int( 'numPoints', default = 8 )
        numPoints.meta['tip'] = "number of sampling points around "\
                              "the elastic peak at a I(tof) curve"

        energyAxis = inv.str( 'energyAxis', default = '20*meV, 200*meV, 0.5*meV' )
        energyAxis.meta['tip'] = (
            'a tuple of (Emin, Emax, dE) to create an axis of neutron energy' \
            'on which the I(E) histogram will be obtained. This I(E) curve should' \
            'show a peak, and the position of that peak is the neutron energy' \
            'we want to compute.'
            )
        
        
        detectorSlice = inv.str( 'detectorSlice', default = "(100,125), ()",
                                 validator = verifyDetectorSlice)
        detectorSlice.meta['tip'] = '''
It is usually not necessary to use all pixels to
compute incident neutron energy. Thousands of pixels should be
pretty good. If you provide detectorSlice argument, a portion of
the I(*,tof) histogram will be used.
For example, suppose a detector system has 200 detectors. and each
detector has 40 pixels. And we want to use the first 25 detectors,
and all 40 pixels of those 25 detectors, then

  detectorSlice = (0,25), ()

The empty bracket means all pixels for every detector.
'''
        
        pass # end of Inventory
    
    
    def __init__(self,name = "IncidentEnergySolver_UseElasticPeaks"):
        base.__init__(self, name)
        return


    def __call__(self, run):
        return self._solver(run)
        

    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.numPoints = si.numPoints
        self.detectorSlice = eval(si.detectorSlice)
        import reduction.units as units
        meV = units.energy.meV
        self.energyAxis = eval(si.energyAxis)
        return


    def _init(self):
        base._init(self)
        from reduction.core.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks as Solver
        self._solver = Solver(
            numPoints = self.numPoints,
            detectorSlice = self.detectorSlice,
            Eaxis = self.energyAxis,
            )
        return

    pass



# version
__id__ = "$Id$"

# End of file 
