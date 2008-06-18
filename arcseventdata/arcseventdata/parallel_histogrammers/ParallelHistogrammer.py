#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

import journal
info = journal.info('histogrammer')
warning = journal.warning('ParallelHistogrammer')


from ParallelComponent import ParallelComponent

class ParallelHistogrammer(ParallelComponent):

    def __call__( self, eventdatafilename, nevents, *args):
        
        mpiRank = self.mpiRank
        mpiSize = self.mpiSize

        if mpiRank == 0:
            info.log( "eventdatafilename = %s" % eventdatafilename )
            info.log( "will process %d neutrons" % nevents )
            pass
        
        import math
        # the number of neutrons that each node need to process
        chunk = int( math.ceil( 1.*nevents/mpiSize ) )
        start = mpiRank * chunk
        info.log('node %d: histogramming...' % (mpiRank, ))
        h = self._run( eventdatafilename, start, chunk, *args)
        info.log('node %d: histogramming done' % (mpiRank, ))

        # send the histogram to the master node
        #  mpi comm channel
        tag = 100
        #  some data
        data = h.data().storage().asNumarray()
        shape = data.shape
        datatype = data.dtype
        from numpy import fromstring

        #  send/receive
        if mpiRank > 0:
            info.log( "%s: sending histogram to master node..." % mpiRank )
            s = data.copy().tostring()
            self.mpiSendStr( s, 0, tag )
            info.log( "%s: histogram sent to master node." % mpiRank )
            return

        for i in range(1, mpiSize):
            datastr = self.mpiReceiveStr( i, tag)
            if len(datastr) == 0:
                raise RuntimeError, 'data string received from node %s is empty. tag = %s' %( i, tag ) 
            data = fromstring(datastr, datatype)
            data.shape = shape
            info.log( "received histogram from node %d" % i )
            h.data().storage().asNumarray()[:] += data
            info.log( "added histogram from node %d into that of node 0" % i )
            continue

        # set error bar squares to be equal to counts
        h.errors().storage().asNumarray()[:] = h.data().storage().asNumarray()

        import os
        info.log( "times: %s" % str(os.times()) )
        return h


    def _run(self, eventdatafilename, start, chunk, *args):
        raise NotImplementedError
    

    pass # end of ParallelHistogrammer
    


# version
__id__ = "$Id$"

#  End of file 
