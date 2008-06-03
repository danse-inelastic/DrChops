#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from FacilityFrontEnd import *

class GetExperimentalRun(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Create "experimental-run" instance out of data source (data files, for example)'
    pass


getRun = GetExperimentalRun()


import measurement.ins as mi
import measurement.ins.LRMECS as lrmecs
getRun.registerEngineFactory(
    'lrmecs', FunctorFromFunction( lrmecs.createRun ) )

import measurement.ins.Pharos as pharos
getRun.registerEngineFactory(
    'pharos', FunctorFromFunction( pharos.createRun ) )

from measurement.ins.ARCS import createRun as arcs
getRun.registerEngineFactory(
    'arcs', FunctorFromFunction( arcs ) )


getRun.select( 'lrmecs' )


__all__ = ['GetExperimentalRun', 'getRun']

# version
__id__ = "$Id$"

# End of file 
