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


from Connectable import Connectable
class Subtract(Connectable):

    def __init__(self, name='subtract'):
        Connectable.__init__(self, name, 'binary operator')
        return

    sockets = {
        'in': [ 'operand1', 'operand2'],
        'out': [ 'result' ],
        }

    def _update(self):
        operand1 = self._getInput( 'operand1' )
        operand2 = self._getInput( 'operand2' )

        result = operand1 - operand2
        
        self._setOutput( 'result', result )
        return

    pass # end of Subtract


# version
__id__ = "$Id$"

# End of file 
