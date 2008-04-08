#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.IdptExtractor
## Extract I(..., det,pix,tof) histograms from an experimental run.
##
## A "run" data object contains information about
## an experimental run:
## instrument components, geometrical information about components,
## all raw data.
## This component extracts the I(d,p,t) histograms from a "run"
## data object.
## I(...,d,p,t) histograms are the most important histograms for
## an experimental run.
## It contains a function of counts measured on a 3-D grid:
## (..., detectorID, pixelID, time-of-flight).
##
## This component supports parallel computing.
##

import journal
debug = journal.debug( 'reduction.core.IdptExtractor' )

from ParallelComponent import ParallelComponent
from reduction.utils.PseudoSingleton import PseudoSingleton


class IdptExtractor(PseudoSingleton, ParallelComponent):

    def __init1__(self, run):
        self._run = run
        debug.log( '%s' % self._run )

        self._getDetectorIDPartition()
        self._idpt = None
        return


    def __call__(self):
        if self._idpt is None:
            self._idpt = self._extract()
            pass
        return self._idpt


    def _extract(self):
        if self.parallel:
            ids = self._detectorIDs
            range = ids[0], ids[-1]
            name = self._detectorLevel0.lower() + 'ID'
            d = {name: range}
            return self._run.getIdpt( **d )
        return self._run.getIdpt()


    def _getDetectorIDPartition(self):
        '''In parallel redcution, we partition the highest
        level detector IDs to partitions for all processors.

        For example, for Pharos instrument, the highest level
        detector is detector. Pharos has more than 100 detectors,
        and they are evenly divided into partitions for each
        processor, and each processor work on a slice of
        Idpt, where Idpt = I(detectorID, pixelID, tof)

        For another example, for ARCS instrument, the highest level
        detector is detector pack. ARCS has about 100 detector packs,
        and they are evenly divided into partitions for each
        processor, and each processor work on a slice of
        Idpt, where Idpt = I(packID, detectorID, pixelID, tof)
        '''
        instrument, geometer = self._run.getInstrument()

        if self.parallel:
            mpiRank = self.mpiRank
            channel = 99
            detectorIDs = self._getHighestLevelDetectorIDs(instrument)
            if mpiRank == 0:
                mpiSize = self.mpiSize
                partitions = _partition( mpiSize, [detectorIDs] )
                for peer in range( 1, mpiSize ):
                    self.mpiSend( partitions[peer], peer, channel )
                    continue
                
                self._detectorIDs = partitions[0]
                pass
            else:
                self._detectorIDs = self.mpiReceive( 0, channel )
                pass
            pass
        return
    

    def _getHighestLevelDetectorIDs(self, instrument):
        detSystem = instrument.getDetectorSystem()
        level0elements = detSystem.elements()
        level0 = level0elements[0].__class__.__name__
        self._detectorLevel0 = level0
        ret = [ e.id() for e in level0elements ]
        return ret

    pass


def _partition( n, lists ):
    ''' partition things in lists to n nodes, return the stuff for node i

    For example
      lists = [ (1,2,3,4,5,6,), (7,8) ]
      n = 4
    partition givens
      (1,2), (3,4), (5,6), (7,8)
      
    Another example
      lists = [ (1,2,3,4,5,6,7), (8,9) ]
      n = 4
    partition givens
      (1,2), (3,4), (5,6,7), (8,9)
      
    '''
    # total number of stuff to partition
    N = sum( [ len(l) for l in lists ] )
    # number of nodes for each l in lists
    nnodes = [ int( len(l)*1.0/N * n + 0.5 )  for l in lists ]
    # make sure total number of nodes matches
    totnnodes = sum(nnodes)
    diff = n - totnnodes
    if diff != 0:
        tmp = list(nnodes); maxnnode = tmp.sort()[-1]
        index = nnodes.index( maxnode )
        newnnode = maxnnode + diff
        if newnnode < 1:
            raise RuntimeError, \
                  "Unable to partition lists %s to %s parts" % (
                lists, n)
        nnodes[index] = newnnode
        pass
    ret = [ _partition1( nnode, l ) for nnode, l in zip( nnodes, lists ) ]
    from operator import add
    return reduce(add, ret)


def _partition1( n, l ):
    ''' partition the list l into n partitions'''
    from math import ceil
    size = int( ceil(len(l)*1./n) )
    return [ l[size*i: size*(i+1)] for i in range(n) ]


def test_partition():
    lists = [ (1,2,3,4,5,6,), (7,8) ]
    n = 4
    assert _partition( n, lists ) ==  [(1,2), (3,4), (5,6), (7,8)]

    lists = [ (1,2,3,4,5,6,9), (7,8) ]
    n = 4
    print _partition( n, lists )
    return


def test():
    test_partition()
    return


if __name__ == '__main__': test()
    

# version
__id__ = "$Id$"

# End of file 
