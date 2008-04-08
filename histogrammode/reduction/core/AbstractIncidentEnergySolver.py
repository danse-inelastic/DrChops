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



## \package reduction.core.AbstractIncidentEnergySolver
## provides uniform interface to calculate neutron incident energy
##
## for direct geometry time of flight instrument, it is an
## important step to determine the incident energy in data reduction.
## There are different ways to do that. Usually there are several monitors
## in an instrument, then
## times of flight when neutrons hit the monitors can be used to determine
## neutron velocity and hence the neutron energy. But there are cases in which
## this
## approach is not applicable. For example, in Pharos, there are no monitors.
## Therefore, we have to calculate incident energy directly from the main
## dataset. This class hides all these details, and only specify the interface
## of an energy solver.




class AbstractIncidentEnergySolver:

    "abstract base class to deterimine incident neutron energy"

    def __call__(self, run):
        """solve incident energy in an experimental run

        @run: experiment run. instance of measurement.Run
        @return: incident energy
        @rtype:  float
        """
        raise NotImplementedError , "%s must provide solve()" % (
            self.__class__.__name__)


    pass #end of AbstractIncidentEnergySolver


# version
__id__ = "$Id$"

# End of file 
