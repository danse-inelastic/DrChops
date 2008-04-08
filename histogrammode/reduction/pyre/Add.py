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
class Add(Connectable):

    def __init__(self, name='add'):
        Connectable.__init__(self, name, 'binary operator')
        return

    sockets = {
        'in': [ 'operand1', 'operand2'],
        'out': [ 'result' ],
        }

    def _update(self):
        operand1 = self._getInput( 'operand1' )
        operand2 = self._getInput( 'operand2' )

        result = operand1 + operand2
        
        self._setOutput( 'result', result )

        return

    pass # end of Add


# version
__id__ = "$Id$"

# End of file 
