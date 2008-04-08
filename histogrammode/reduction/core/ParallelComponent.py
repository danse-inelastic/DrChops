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


## \package reduction.core.ParallelComponent
## Supports for parallel computing


import journal
info = journal.info( 'mpi' )


class ParallelComponent(object):

    '''Base class for operators that can be parallelized.
    '''

    try:
        import mpi
        world = mpi.world()
        mpiRank = world.rank; mpiSize = world.size
        if mpiSize < 1:
            parallel = False
        else:
            parallel = True
    except:
        mpiRank = 0
        mpiSize = 1
        parallel = False
        pass


    def runMasterNodeOnly(self, channel, func, *args, **kwds):
        if self.parallel:
            if self.mpiRank == 0:
                ret = func( *args, **kwds )
                for i in range( 1, self.mpiSize ):
                    self.mpiSend( ret, i, channel )
                    continue
                pass
            else:
                ret = self.mpiReceive( 0, channel )
                pass
            return ret
        return func(*args, **kwds)

    
    def mpiSend( self, obj, peer, tag):
        world = self.world
        s = pickle.dumps( obj )
        port = world.port(peer=peer, tag=tag)
        port.send(s)
        msg = "Machine %s: sent %s to peer %s with tag %s" % (
            self.mpiRank, obj, peer, tag) 
        info.log( msg )
        return


    def mpiReceive(self, peer, tag):
        world = self.world
        port = world.port(peer=peer, tag=tag)
        message = port.receive()
        obj = pickle.loads( message )
        msg = "Machine %s: received %s from peer %s with tag %s" % (
            self.mpiRank, obj, peer, tag)
        info.log( msg )
        return obj


import pickle
    


# version
__id__ = "$Id$"

# End of file 
