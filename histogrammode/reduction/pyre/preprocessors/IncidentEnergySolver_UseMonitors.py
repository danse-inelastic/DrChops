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


## \package reduction.pyre.IncidentEnergySolver_UseMonitors
## Use monitor data to calculate incident neutron energy



from AbstractIncidentEnergySolver import AbstractIncidentEnergySolver as base


class IncidentEnergySolver_UseMonitors(base):
    
    """
    An implementation of EiSolver that calcualte Ei from data of two monitors.
    """

    class Inventory(base.Inventory):

        import pyre.inventory as inv
        import reduction.pyre.inventory as localinv

        monitor1Id = inv.int( 'monitor1Id', default = 0 )
        monitor1Id.meta['tip'] = "ID of monitor #1"

        monitor1FitGuess = localinv.numberlist(
            'monitor1FitGuess', default = [0.0, 0.0, 0.0, 0.0] )
        monitor1FitGuess.meta['tip'] = "Guess of parameters of the peak "\
            "used to fit monitor data #1: (position, width, intensity, offset)"

        monitor2Id = inv.int( 'monitor2Id', default = 1 )
        monitor2Id.meta['tip'] = "ID of monitor #2"

        monitor2FitGuess = localinv.numberlist(
            'monitor2FitGuess', default = [0.0, 0.0, 0.0, 0.0] )
        monitor2FitGuess.meta['tip'] = "Guess of parameters of the peak "\
            "used to fit monitor data #2: (position, width, intensity, offset)"

        pass # end of Inventory
    
    
    def __init__(self,name = "IncidentEnergySolver_UseMonitors"):
        base.__init__(self, name)
        return


    def __call__(self, run):
        return self._solver(run)
        

    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.monitor1Id = si.monitor1Id
        self.monitor1FitGuess = si.monitor1FitGuess
        self.monitor2Id = si.monitor2Id
        self.monitor2FitGuess = si.monitor2FitGuess
        return


    def _init(self):
        from reduction.core.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as Solver
        self._solver = Solver(
            monitor1Id = self.monitor1Id,
            monitor2Id = self.monitor2Id,
            monitor1FitGuess = self.monitor1FitGuess,
            monitor2FitGuess = self.monitor2FitGuess,
            )
        return

    pass



# version
__id__ = "$Id: IncidentEnergySolver_UseMonitors.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
