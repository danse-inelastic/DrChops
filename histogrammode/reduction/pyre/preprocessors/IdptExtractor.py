#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.pyre.preprocessors.IdptExtractor


from Connectable import Connectable as base

class IdptExtractor(base):

    sockets = {
        'in': ['run'],
        'out': ['Idpt'],
        }


    def __init__(self, name = 'IdptExtractor' ):
        base.__init__(self, name, facility = 'IdptExtractor' )
        return

    
    def _update(self):
        r = self._getInput('run')
        from reduction.core.IdptExtractor import IdptExtractor
        h = IdptExtractor(r)()
        self._setOutput( 'Idpt', h )
        return
    

    pass # end of IdptExtractor


# version
__id__ = "$Id$"

# End of file 
