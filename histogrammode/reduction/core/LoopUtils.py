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



##\package reduction.core.LoopUtils
#provides algorithm to loop over all detectors and do some calculation



from instrument.elements.DetectorVisitor import DetectorVisitor as base
class DetectorVisitor(base):
    def onSampleAssembly(self, sampleassembly): return


class HistogramProcessor:

    """This processor process a histogram by looping over detectors
    """

    def __init__(self, mask):
        self.mask = mask
        return


    def onDetector(self, detID, histogram):
        raise NotImplementedError


    def run(self, histograms):
        
        for hist in histograms.getAll():
            
            for detID in hist.axisFromName('detectorID').binCenters():
                
                if self.mask.include( detID ): continue

                histSlice = hist[detID, (), ()]
                self.onDetector( detID, histSlice )
                
                continue
            continue
        
        return


    pass # end of class Processor



class HistogramProcessor2:


    def onPoint(self, X):
        raise NotImplementedError


    def run(self, axes):
        
        count = 0
        shape = [ axis.size() for axis in axes ]
        v = volume( shape )
        axisCenters = [axis.binCenters() for axis in axes]
        axisNames = [axis.name() for axis in axes]
        indexes = [ 0 for i in range(len(shape)) ]
        
        while count < v:
            X = {}
            for i, axis, name in zip( indexes, axisCenters, axisNames) :
                X[name] = axis[i]
                
            self.onPoint( X )
            increment( indexes, shape )
            count += 1
            continue

        return


def volume(shape):
    from operator import mul
    return reduce(mul, shape)


def increment( indexes, limits ):
    """increase indexes up to limits
    increment( [1,4,3], [3,10,8] ) --> indexes becomes [2,4,3]
    increment( [2,4,3], [3,10,8] ) --> indexes becomes [0,5,3]
    """
    for i, index in enumerate(indexes):
        if index < limits[i]-1:
            indexes[i] += 1
            break
        else :
            indexes[i] = 0


    
# version
__id__ = "$Id: LoopUtils.py 1415 2007-09-29 07:57:40Z linjiao $"

# End of file 
