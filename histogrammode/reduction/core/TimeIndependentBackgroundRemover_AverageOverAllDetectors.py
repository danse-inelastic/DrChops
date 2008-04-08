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


## \package reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors
## An implementation of AbstractTimeIndependentBackgroundRemover.
##
## remove tof-independent background from data
##
## It calculates
## background by averaging over all detectors.
##



class TimeIndependentBackgroundRemover_AverageOverAllDetectors:

    """This component is used to remove "time-independent background".

    The user specify the tof range that will be regarded as "time-independent
    background". This component will calculate the average intensity
    in those tof channels and the average will be removed.

    This implementation is different from TimeIndependentBackgroundRemover
    in that the latter averages background counts in every detector.
    """


    def __init__(self, tbgMin=5000., tbgMax=5500.):
        '''__init__(tbgMin, tbgMax)

        tbgMin, tbgMax: the tof window from which the background is
          calculated.
        '''
        if tbgMin >= tbgMax:
            self._nowindow = True
            self._bg = self._bgerr = 0
            return
        self._nowindow = False
        self.tbgMin = tbgMin
        self.tbgMax = tbgMax
        return 


    def __call__(self, hists_or_hist, mask=None):
        """ remove time-independent background

        hists_or_hist: a histogram container object or a histogram
        mask: detector mask
        """
        if self._nowindow: return #nothing to do
        
        if mask is None:
            from instrument.DetectorMask import DetectorMask
            mask = DetectorMask()
            pass # end if mask is None
        
        from histogram import histogramContainer, histogram
        from numpy import ones
        from ApplyMaskToHistogram import applyMask
        
        hists = histogramContainer( hists_or_hist )
        
        tbgMin = self.tbgMin
        tbgMax = self.tbgMax

        bg, bgerr = 0, 0
        n = 0
        for hist in hists:
            tofaxis = hist.axisFromName( 'tof' )
            tconversion = microsecond/tofaxis.unit()

            h = hist[ {'tof': (tbgMin*tconversion, tbgMax*tconversion) } ]
            
            detaxes = h.axes()[:-1]
            
            b, be = h.sum()
            bg += b
            bgerr += be

            masked = histogram( 'masked', detaxes )
            masked[ {} ] = ones( masked.shape() ), None
            applyMask( mask, masked )
            
            n += masked.sum()[0] * h.axisFromName('tof').size()
            continue
        bg/=n; bgerr/=n*n
        for hist in hists: hist -= bg, bgerr
        self._bg = bg; self._bgerr = bgerr
        return


    def bg(self):
        """bg() --> background to be removed
        return value is a tuple: (bg, bgerr)
        """
        d = self.__dict__
        bg = d.get('_bg'); bgerr = d.get('_bgerr')
        if bg is not None and bgerr is not None: return bg, bgerr
        raise RuntimeError , "Must run method 'process' first"


import reduction.units as units
microsecond = units.time.microsecond



# implementation details
from reduction.LoopUtils import HistogramProcessor
class BGAccumulator(HistogramProcessor):

    def __init__(self, mask, tbgMin, tbgMax):

        HistogramProcessor.__init__(self, mask)
        
        self.tbgMin = tbgMin;  self.tbgMax = tbgMax
        
        import journal
        channel = "BGAccumulator"
        self._error = journal.error( channel )
        self._debug = journal.debug( channel )
        self._info = journal.info( channel )
        return


    def run(self, histograms):
        #results
        self._npxls = 0
        from numpy import array
        self._totbg = array( [0.,0.] )

        tofAxis = histograms().axisFromName( 'tof' )
        dtof = tofAxis[1] - tofAxis[0]
        self.nTbgChannels = (self.tbgMax-self.tbgMin)/dtof + 1

        HistogramProcessor.run(self, histograms )
        return


    def onDetector(self, detID, histogram):
        mask = self.mask
        if mask.include( detID ): return

        self._debug.log( "onDetector: %s" % detID )

        pixelAxis = histogram.axisFromName( 'pixelID' )

        min, max = self.tbgMin, self.tbgMax
        
        for pixelID in pixelAxis.binCenters():
            if mask.include( detID, pixelID ): continue
            histSlice = histogram[ pixelID, (min, max) ]
            self._npxls += 1
            cnts, error = histSlice.sum()
            self._totbg += [cnts, error]
            continue


    def result(self):
        norm = self._npxls * self.nTbgChannels
        bg, err = self._totbg
        bg, err = bg/norm, err/norm/norm
        self._debug.log("norm: %s, average background: %s, %s" % (norm, bg,err))
        return bg, err
    
    pass



class TBGProcessorPerDet(HistogramProcessor):


    def __init__(self, mask):
        HistogramProcessor.__init__(self, mask)
        import journal
        channel = "TBGProcessorPerDet"
        self._error = journal.error( channel )
        self._debug = journal.debug( channel )
        self._info = journal.info( channel )
        return


    def run(self, histograms, bg, bgerr):
        self.bg = bg
        self.bgerr = bgerr
        HistogramProcessor.run(self, histograms)
        return


    def onDetector(self, detectorID, histogram):
        mask = self.mask
        if mask.include( detectorID ): return
        self._info.log("remove background from data of detector %s" % detectorID)
                
        histogram -= self.bg, self.bgerr
        return
            
    pass # end of TBGProcessorPerDet



# version
__id__ = "$Id$"

# End of file 
