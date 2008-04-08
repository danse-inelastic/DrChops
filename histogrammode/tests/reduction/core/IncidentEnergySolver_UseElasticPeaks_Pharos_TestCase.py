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


import journal


from reduction.core.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks as Solver, debug, info



import unittestX as unittest


class IncidentEnergySolver_UseElasticPeaks_TestCase(unittest.TestCase):


    def test(self):
        """IncidentEnergySolver_UseElasticPeaks
        """
        from measurement.ins.Pharos import createRun as  createPharosRun
        run = createPharosRun( '../../ins-data/Pharos/PharosDefinitions.txt',
                               '../../ins-data/Pharos/Pharos_342.nx.h5' )
        
        eiSolver = Solver( Eaxis = (70*meV, 80*meV, 0.01*meV ),
                           detectorSlice = ( (150,200),() ),
                           )
        eiSolved = eiSolver( run )

        print eiSolved/meV
        self.assertAlmostEqual( eiSolved/meV, 75, 0 )

        import os
        print os.times()
        return
    

    pass # end of IncidentEnergySolver_UseElasticPeaks_TestCase

from pyre.units.energy import meV

    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_UseElasticPeaks_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    global info
    info.activate()
    #debug.activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##     journal.debug('IncidentEnergySolver_UseElasticPeaks').activate()
##     journal.debug('reduction.histCompat').activate()
##     journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: IncidentEnergySolver_UseElasticPeaks_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
