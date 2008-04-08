#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.pyre.Spe2Sqe
## Convert S(phi,E) to S(Q,E)


from Connectable import Connectable as base

from Axis import Axis


class Spe2Sqe(base):


    """convert S(phi,E) to S(Q,E)

    The only input needed is the Q axis on which the output
    S(Q,E) histogram should be built.
    """


    class Inventory(base.Inventory):

        import pyre.inventory as inv
        # |Q| range
        QAxis = inv.facility(
            "QAxis", factory = Axis,
            args = ['Q', 0.0, 11.0, 0.2, 'angstrom**-1'] )
        QAxis.meta['tip'] = "Q axis. unit: A^-1"
	pass


    def __call__(self, ei, sphiEHist, QAxis = None):
        """convert s(phi,E) histogram to S(Q,E) histogram

        \arg ei incident energy
        \arg sphiEHist S(phi,E) histogram
        \arg QAxis Q axis
        """
        if QAxis is None: QAxis = self.QAxis
        return self.engine( ei, sphiEHist, QAxis )


    sockets = {
        'in': ['QAxis', 'Ei', 'spe'],
        'out': ['sqe'],
        }


    def _update(self):
        spe = self._getInput( 'spe' )
        Ei = self._getInput( 'Ei' )
        QAxis = self._getInput( 'QAxis' )

        sqe = self( Ei, spe, QAxis )
        
        self._setOutput( 'sqe', sqe )
        return

    
    def __init__(self, name = None):
        if name is None: name = 'Spe2Sqe'
        base.__init__(self, name, facility='convert s(pe) to s(qe)')
        return


    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.QAxis = si.QAxis #component
        return


    def _init(self):
        base._init(self)
        self.QAxis = self.QAxis() # Axis instance
        self.setInput( 'QAxis', self.QAxis )

        from reduction.core.Spe2Sqe import Spe2Sqe
        self.engine = Spe2Sqe( )
        return


    pass # end of Spe2Sqe



# version
__id__ = "$Id: Spe2Sqe.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
