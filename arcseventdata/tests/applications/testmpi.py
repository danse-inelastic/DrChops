# to run this test
# mpirun -n 3  mpipython.exe testmpi.py

import mpi
world = mpi.world()
mpiRank = world.rank; mpiSize = world.size

N = 10
tag = 999

import numpy
a = numpy.zeros( N )

s = a.tostring()
#s = 'hello'

if mpiRank > 0:
    port = world.port(peer=0, tag=tag )
    port.send(s)
    print 'node %d, sent %d' % (mpiRank, len(s) )
    
else:
    for node in range(1, mpiSize):
        port = world.port( peer=node, tag=tag )
        s = port.receive()
        print 'node0: received %s from node %d' %  (len(s), node) 
        continue

    
