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

class Idpt2Sqe(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Convert I(det,pix,tof) to S(Q,E)'
    pass


idpt2sqe = Idpt2Sqe()


from reduction.core.Idpt2Sqe import Idpt2Sqe

idpt2sqe.registerEngineFactory('default',  Idpt2Sqe)


idpt2sqe.select( 'default' )


__all__ = ['Idpt2Sqe', 'idpt2sqe']



# version
__id__ = "$Id$"

# End of file 
