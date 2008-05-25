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



from _utils import getModules
modules = getModules()
del getModules

for m in modules:
    try:
        all = m.__all__
    except:
        continue
    for k in all:
        exec '%s = m.%s' % (k, k)
        continue
    continue

del k, all, m, modules


def redcmds():
    """a list of reduction commands"""
    g = globals()
    class ReductionCommands : pass
    for i in g:
        if not isinstance( g[i], FacilityFrontEnd ): continue
        cmd = '''
def %s(*args, **kwds): return
f = %s''' % (i, i)
        exec cmd
        f.__doc__ = g[i].onelinehelp
        setattr(ReductionCommands, i, f )
        continue
    help( ReductionCommands )
    return


#misc things
#from instrument.elements.samples import vanadiumPlate
from sampleassembly.predefined import vanadiumPlate
from reduction.core.ApplyMaskToHistogram import applyMask
from reduction.histCompat import functors
from reduction import units


# version
__id__ = "$Id$"

# End of file 
