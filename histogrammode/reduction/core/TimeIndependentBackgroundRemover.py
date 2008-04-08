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


## \package reduction.core.TimeIndependentBackgroundRemover
## An implementation of AbstractTimeIndependentBackgroundRemover.
##
## Remove tof-independent background.
## This remover calculates averaged counts in a user-specified
## tof window for each detector, and then subtract that from
## the I(tof) for each pixel on the detector.


from AbstractTimeIndependentBackgroundRemover import AbstractTimeIndependentBackgroundRemover as Base

class TimeIndependentBackgroundRemover( Base ):

    '''Remove time-independent background from measured histogram

    This remover calculates averaged counts in a user-specified
    tof window for each detector, and then subtract that from
    the I(tof) for each pixel on the detector.
    '''

    def __init__(self, tbgMin=5000, tbgMax=5500):
        '''__init__(tbgMin, tbgMax)

    tbgMin, tbgMax: the tof window from which the background is
      calculated.
        '''
        self.tbgMin = tbgMin
        self.tbgMax = tbgMax
        return 


    def __call__(self, hists_or_hist, mask = None):
        """ __call__( hists_or_hist, instrument, mask ):
    remove time-independent background

    inputs:
        hists_or_hist: a histogram container object or a histogram
        mask: detector mask
        """
        if mask is None:
            from instrument.DetectorMask import DetectorMask
            mask = DetectorMask()
            pass # end if mask is None
        
        from histogram import histogramContainer
        hists = histogramContainer( hists_or_hist )
        
        tbgMin = self.tbgMin
        tbgMax = self.tbgMax
        
        tbgp = TBGProcessor(mask, tbgMin, tbgMax)
        tbgp.run(hists)
        self._bgs = tbgp.bgs()
        return
    

    def bg(self):
        """bg() --> background to be removed
        return value is a dictionary of {detID: (bg, bgerr)}
        """
        d = self.__dict__
        bgs = d.get('_bgs')
        if bgs is not None: return bgs
        raise RuntimeError , "Must run method 'process' first"


    pass # end of TimeIndependentBackgroundRemover



#implementation details
from reduction.LoopUtils import HistogramProcessor
class TBGProcessor(HistogramProcessor):

    def __init__(self, mask, tbgMin, tbgMax):
        
        HistogramProcessor.__init__(self, mask)

        self.tbgMin = tbgMin
        self.tbgMax = tbgMax

        import journal
        channel = "TBGProcessor"
        self._error = journal.error( channel )
        self._debug = journal.debug( channel )
        self._bgs = {}
        return


    def onDetector( self, detID, histogram ):
        #shall we consider the "singles" in mask?
        mask = self.mask
        if mask.include(detID): return
        
        bgSlice = histogram[ (), (self.tbgMin, self.tbgMax) ]
        bg, bgerr = bgSlice.average()
        
        histogram -= bg, bgerr
        self._bgs [ detID ] = bg, bgerr
        return


    def bgs(self): return self._bgs
    
        
    pass # end of class TBGProcessor


# version
__id__ = "$Id: TimeBGround.py 1212 2006-11-21 21:59:44Z linjiao $"

# End of file 
