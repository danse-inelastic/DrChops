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



## \package reduction.pyre.AbstractIncidentEnergySolver
## provides uniform interface to calculate neutron incident energy
##
## For direct geometry time of flight instrument, it is an
## important step to determine the incident energy in data reduction.
## There are different ways to do that. Usually there are several monitors
## in an instrument, then
## times of flight when neutrons hit the monitors can be used to determine
## neutron velocity and hence the neutron energy. But there are cases this
## approach is not applicable. For example, in Pharos, there are no monitors.
## Therefore, we have to calculate incident energy directly from the main
## dataset. This class hides all these details, and only specify the interface
## of an energy solver.




from Connectable import Connectable as base


class AbstractIncidentEnergySolver(base):

    "abstract base class for pyre component to deterimine incident neutron energy"

    class Inventory(base.Inventory):
        pass


    def __init__(self, name):
        base.__init__(self, name, facility='incident energy solver')
        return
    

    def __call__(self, run):
        """solve incident energy in an experimental run
        @return: incident energy
        @rtype:  float
        """
        raise NotImplementedError , "%s must provide solve()" % (
            self.__class__.__name__)


    sockets = {
        'in': ['run'],
        'out': ['Ei'],
        }


    def _update(self):
        r = self._getInput('run')
        ei = self( r )
        self._setOutput('Ei', ei )
        return


    pass #end of AbstractIncidentEnergySolver


# version
__id__ = "$Id: AbstractIncidentEnergySolver.py 1146 2006-09-27 17:31:51Z linjiao $"

# End of file 
