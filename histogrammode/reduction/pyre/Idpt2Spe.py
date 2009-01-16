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


## \package reduction.pyre.Idpt2Spe
## An implemenation of Idpt2Spe


from AbstractIdpt2Spe import AbstractIdpt2Spe

class Idpt2Spe(AbstractIdpt2Spe):


    """ reduce I(det, pix, tof) to S(phi,E) histogram

    This reducer needs inputs about the two axes on which
    the output histogram S(phi,E) will be produced: phi (scattering angle)
    and E (energy transfer).
    """


    class Inventory(AbstractIdpt2Spe.Inventory):
        import pyre.inventory as inv
        pass # end of Inventory
        

    def __init__(self, name = "Idpt2Spe"):
        AbstractIdpt2Spe.__init__(self, name)
        import journal
        self._warning = journal.warning( name )
        return


    def __call__(self, ei, histogram, instrument, geometer, **kwds):
        reducer = self.engine
        return reducer( ei, histogram, instrument, geometer, **kwds )
        #c_and_Js = []
        #for h in histograms:
        #print h
        #reducer.reduce_( ei, h, instrument, geometer ) )
        #c_and_Js.append(reduced )
        #continue
        #from reduction.core.HistogramCombiner import combine
        #return combine( c_and_Js )
        

    sockets = {
        'in': ['Ei', 'Idpt', 'instrument', 'mask'],
        'out': ['spe'],
        }


    def _update(self):
        Ei = self._getInput( 'Ei' )
        Idpt = self._getInput( 'Idpt' )
        instrument, geometer = self._getInput('instrument')
        mask = self._getInput('mask')

        from reduction import units
        self._debug.log('Ei=%s meV' % (Ei/units.energy.meV))
        
        spe = self( Ei, Idpt, instrument, geometer, mask = mask )

        self._setOutput( 'spe', spe )
        return
    

    def _configure(self):
        AbstractIdpt2Spe._configure(self)
        si = self.inventory   # handy alias
        return


    def _init(self):
        AbstractIdpt2Spe._init(self)
        from reduction.core.Idpt2Spe_a import Idpt2Spe_a
        self.engine = Idpt2Spe_a(
            EAxis = self.EAxis,
            phiAxis = self.phiAxis,
            mask = self.mask )
        self.setInput('mask', self.mask)
        return



# version
__id__ = "$Id: Idpt2Spe.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
