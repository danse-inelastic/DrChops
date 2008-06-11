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


from reduction.core.Idpt2Spe_a import Idpt2Spe_a as base
class Engine(base):
    __doc__ = base.__doc__
    def __call__(self, ei, idpt , i = None, g = None, run = None):
        '''idpt2spe(ei, idpt, run=None): convert I(...,pixel,tof) to S(phi,E)

        ei: incident energy
        idpt: I(..., pixel, tof) histogram. "..." indicates additional detector
              axes such as packs, tubes, etc
        run: The experimental run instance. 
        '''
        # i and g are kept for backward compatibility
        if run: i,g = run.getInstrument()
        else:
            import warnings
            warnings.warn( 'idpt2spe( ei, idpt, instrument, geometer ) deprecated. use idpt2spe(ei, idpt, run=run)', DeprecationWarning )
        return base.__call__(self, ei, idpt, i, g)
        

idpt2spe.registerEngineFactory('default',  Engine)


idpt2spe.select( 'default' )


__all__ = ['Idpt2Spe', 'idpt2spe']



# version
__id__ = "$Id$"

# End of file 
