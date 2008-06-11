#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from FacilityFrontEnd import *

class Spe2Sqe(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Convert S(phi,E) to S(Q,E)'
    pass


spe2sqe = Spe2Sqe()


from reduction.core.Spe2Sqe import Spe2Sqe

spe2sqe.registerEngineFactory('default',  Spe2Sqe)


spe2sqe.select( 'default' )


__all__ = ['Spe2Sqe', 'spe2sqe']



# version
__id__ = "$Id$"

# End of file 
