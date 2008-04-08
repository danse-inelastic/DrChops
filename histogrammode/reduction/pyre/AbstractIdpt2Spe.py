#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                       (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.pyre.AbstractIdpt2Spe
## provides base class for reduction I(det,pix,tof) --> S(phi,E) 


from Axis import Axis
from PhiAxis import PhiAxis
from Mask import Mask



from Connectable import Connectable as base


class AbstractIdpt2Spe(base):


    """ reduce I(det, pix, tof) to S(phi,E) histogram

    This is the abstact base class of reducers that reduce
    I(det, pix, tof) to S(phi,E) histogram
    """


    class Inventory(base.Inventory):
        import pyre.inventory as inv

        mask = inv.facility( 'mask', factory = Mask)
        mask.meta['tip'] = 'detector mask'
        mask.meta['opacity'] = 1000
        
        # energy range, etc. (Must agree with ERebinner)
        EAxis = inv.facility(
            "EAxis", factory = Axis,
            args = ['energy', -50.0, 50.0, 1.0, 'meV'] )
        EAxis.meta['tip'] = "energy axis. unit: meV"

        # phi range, etc. (Must agree with ERebinner)
        phiAxis = inv.facility(
            "phiAxis", factory = PhiAxis,
            args = ["phi", 2.0, 102.0, 2.0, 'degree'])
        phiAxis.meta['tip'] = "scattering angle axis. unit: degrees"
        pass
        

    def __init__(self, name):
        base.__init__(self, name, facility='reduce raw data to S(phi, E)')
        return


    def __call__(self,  ei, histograms, instrument, geometer):
        """reduce I(det, pix, tof) to S(phi,E) histogram

        \arg ei incident neutron energy
        \arg histograms histogram (I(det,pix,tof)) collection to be reduced
        \arg instrument instrument python representation
        \arg geometer geometer who measures distances, angles, etc
        """
        raise NotImplementedError , "%s must override __call__" % (
            self.__class__.__name__)


    sockets = {
        'in': ['Idpt', 'Ei', 'mask', 'instrument'],
        'out': ['spe'],
        }

    def _update(self):
        Idpt = self._getInput('Idpt')
        Ei = self._getInput('Ei')
        mask = self._getInput('mask')
        instrument, geometer = self._getInput('instrument')
        spe = self(  Ei, Idpt, instrument, geometer)
        self._setOutput( 'spe', spe )
        return
    

    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.EAxis = si.EAxis
        self.phiAxis = si.phiAxis
        self.mask = si.mask
        return


    def _init(self):
        base._init(self)
        self.EAxis = self.EAxis()
        self.phiAxis = self.phiAxis()
        self.mask = self.mask()
        self.setInput( 'mask', self.mask )
        return
    

# version
__id__ = "$Id: AbstractIdpt2Spe.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
