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


## \package reduction.pyre.SqeReducer
## An implemenation of SqeReducer


from SpeReducer import SpeReducer
from Spe2Sqe import Spe2Sqe


from Composite import Composite  as base


class SqeReducer(base):


    """Reduce experimental data to S(Q,E)

    This reducer consists of a SpeReducer component and a Spe2Sqe component.
    """


    class Inventory(base.Inventory):
        import pyre.inventory as inv

        SpeReducer = inv.facility( 'SpeReducer', factory = SpeReducer )
        Spe2Sqe = inv.facility( 'Spe2Sqe', factory = Spe2Sqe )

        pass # end of Inventory
        

    connections = [
        'SpeReducer:Ei->Ei:Spe2Sqe',
        'SpeReducer:spe->spe:Spe2Sqe',
        'Spe2Sqe:sqe->sqe:self',
        'SpeReducer:Ei->Ei:self',
        ]

        
    sockets = {
        'in': [],
        'out': ['sqe', 'Ei'],
        }


    def __init__(self, name = "SqeReducer"):
        base.__init__(self, name)
        return

    pass # end of SqeReducer


# version
__id__ = "$Id: SqeReducer.py 1300 2007-07-09 14:14:07Z linjiao $"

# End of file 
