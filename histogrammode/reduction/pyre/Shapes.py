#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.pyre.Shapes
## pyre compoents for shapes used in reduction package

import journal

from pyre.components.Component import Component
from pyre.geometry.solids.Block import Block as _Block

class Block( Component ):

    """A block is defined by its diagonal (x,y,z)

    This "Block" pyre component is a wrapper of pyre.geometer.solids.Block.
    It defins a "Block" shape.
    """

    class Inventory(Component.Inventory):

        import pyre.inventory as inv
        import inventory as localinv
        diagonal = localinv.numberlist( "diagonal", default = [1.,1.,1.] )
        diagonal.meta['tip'] = "Diagonal dimensions of this block"

        pass # end of Inventory


    def identify(self, visitor): return self._handle.identify(visitor)


    def __init__(self, diagonal = [1.,1.,1.], name = "block", facility = "shape"):
        Component.__init__(self, name, facility)
        self._firewall = journal.firewall(name)
        self.inventory.diagonal = diagonal
        return


    def _configure(self):
        Component._configure(self)
        diagonal = self.inventory.diagonal
        if len(diagonal) != 3:
            self._firewall.log( "diagonal must be a 3-element list: %s" % diagonal)
            pass
        for i, e in enumerate(diagonal):
            if not isinstance(e, int) and not isinstance(e, float):
                try: diagonal[i] = eval(e)
                except: self._firewall.log( "diagonal element must be numbers: %s" % diagonal)
                pass
            continue
        self._handle = _Block(diagonal)
        return

    pass # end of Block



def test():
    b = Block( )
    b._configure()
    class Visitor :
        def onBlock(self, block): return block.diagonal
        pass
    v = Visitor()
    assert b.identify( v ) == b._handle.diagonal

    b = Block()
    b.inventory.diagonal = ['a', 1,2]
    try: b._configure()
    except journal.diagnostics.Diagnostic.Diagnostic.Fatal: print "good. catch input error"
    
    b = Block()
    b.inventory.diagonal = [0, 1,2,4]
    try: b._configure()
    except journal.diagnostics.Diagnostic.Diagnostic.Fatal: print "good. catch input error"
    print "test of Block passed"
    return
                             
if __name__ == '__main__': test()

# version
__id__ = "$Id: VCalib_Det.py 873 2006-04-23 07:50:11Z jiao $"

# End of file 
