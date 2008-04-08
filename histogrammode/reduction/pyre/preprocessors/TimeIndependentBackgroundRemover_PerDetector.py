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


## \package reduction.pyre.TimeIndependentBackgroundRemover_PerDetector
## remove tof-independent background



from AbstractTimeIndependentBackgroundRemover import AbstractTimeIndependentBackgroundRemover as base


class TimeIndependentBackgroundRemover_PerDetector(base):


    from reduction.core.TimeIndependentBackgroundRemover import TimeIndependentBackgroundRemover as Engine

    __doc__ = Engine.__doc__


    sockets = base.sockets.copy()
    sockets['in'].append( 'tofWindow' )
    
    
    class Inventory( base.Inventory ):

        import pyre.inventory as inv
        
        tbgMin = inv.float('tbgMin', default = 5000)
        tbgMin.meta['tip'] = "Minimum  for time-independent background"
        tbgMax = inv.float('tbgMax', default = 5500)
        tbgMax.meta['tip'] = "Maximum  for time-independent background"
        
        pass # end of Inventory


    def __init__(self,
                 name = "TimeIndependentBackgroundRemover_PerDetector"
                 ):
        
        base.__init__(self, name)
        
        return


    def _update(self):
        ''' remove time-independent background
        '''
        mask = self._getInput('mask')
        histogram = self._getInput( 'histogram' )
        tofWindow = self._getInput( 'tofWindow' )

        tbgMin, tbgMax = tofWindow

        remover = self.Engine( tbgMin, tbgMax )
        remover( histogram, mask )
        self._bgs = remover.bg()

        self._setOutput( 'histogram', histogram )
        return    


    def bg(self):
        '''bg() --> background to be removed
        return value is a dictionary of {detID: (bg, bgerr)}
        '''
        return self._bgs


    def _configure(self):
        base._configure(self)
        si = self.inventory
        self.tbgMin = si.tbgMin
        self.tbgMax = si.tbgMax
        return


    def _init(self):
        base._init(self)
        self.setInput( 'tofWindow', (self.tbgMin, self.tbgMax ) )
        return
    
    pass # end of TimeIndependentBackgroundRemover_PerDetector




# version
__id__ = "$Id: TimeIndependentBackgroundRemover_PerDetector.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file 
