#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittestX as unittest
import journal

debug = journal.debug( "IdptExtractor_TestCase" )


from reduction.core.IdptExtractor import IdptExtractor



class IdptExtractor_TestCase(unittest.TestCase):
     
    def test1(self):
        "IdptExtractor: Lrmecs"
        from measurement.ins.LRMECS import createRun as createLrmecsRun
        run = createLrmecsRun( '../../ins-data/Lrmecs/4849' )
        extractor = IdptExtractor( run )
        extractor()
        return


    def test2(self):
        "IdptExtractor: Pharos"
        from measurement.ins.Pharos import createRun as createPharosRun
        run = createPharosRun( '../../ins-data/Pharos/PharosDefinitions.txt',
                               '../../ins-data/Pharos/Pharos_342.nx.h5' )
        extractor = IdptExtractor( run )
        extractor()
        return


    def test3(self):
        "IdptExtractor: MCSimulation"
        from measurement.ins.MCSimulation import createRun 
        run = createRun( '../../ins-data/simulation/SimOutput-ARCS-Ei60-E20-Q5-tof(0.8,1.6,0.01)ms-ncount1000-buffersize100' )
        extractor = IdptExtractor( run )
        extractor()
        return

    def test3a(self):
        "IdptExtractor: MCSimulation, parallel"
        datadir = '../../ins-data/simulation/SimOutput-ARCS-Ei60-E20-Q5-tof(0.8,1.6,0.01)ms-ncount1000-buffersize100'
        pycmd = '''
from measurement.ins.MCSimulation import createRun
run = createRun(%r)
from reduction.core.IdptExtractor import IdptExtractor
extractor = IdptExtractor( run )
h = extractor()
import mpi
print mpi.world().rank
print h.axisFromId(1).binCenters()
''' % datadir
        import tempfile
        pyf = tempfile.mktemp()
        open( pyf, 'w' ).write( pycmd )
        import os
        cmd ='mpirun -n 2 mpipython.exe %s' % pyf
        print cmd
        os.system(  cmd )
        return

    pass 
     
    
def curdir():
    import os
    return os.path.dirname( __file__ )
     
    
def pysuite():
    suite1 = unittest.makeSuite(IdptExtractor_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    debug.activate()
    #from reduction.core.IdptExtractor import debug
    #debug.activate()

    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
