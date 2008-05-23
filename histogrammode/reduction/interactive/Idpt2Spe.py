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

class Idpt2Spe(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        ]
    onelinehelp = 'Convert I(det,pix,tof) to S(phi,E)'
    pass


idpt2spe = Idpt2Spe()


from reduction.core.Idpt2Spe_a import Idpt2Spe_a

idpt2spe.registerEngineFactory('default',  Idpt2Spe_a)


idpt2spe.select( 'default' )


__all__ = ['Idpt2Spe', 'idpt2spe']



# version
__id__ = "$Id$"

# End of file 
