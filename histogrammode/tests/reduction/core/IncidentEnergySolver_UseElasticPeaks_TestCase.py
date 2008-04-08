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
debug = journal.debug( "IncidentEnergySolver_UseElasticPeaks" )


from reduction.core.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks as Solver



import unittestX as unittest


class IncidentEnergySolver_UseElasticPeaks_TestCase(unittest.TestCase):


    def test(self):
        """IncidentEnergySolver_UseElasticPeaks
        """
        from TestRun_for_IncidentEnergySolverUsingElasticPeaks import Run, ei
        run = Run()
        
        eiSolver = Solver( Eaxis = (ei-10*meV, ei+10*meV, 0.01*meV ) )
        eiSolved = eiSolver( run )
        
        self.assertAlmostEqual( ei/eiSolved, 1., 3 )
        return

    pass # end of IncidentEnergySolver_UseElasticPeaks_TestCase


from pyre.units.energy import meV
    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_UseElasticPeaks_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
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
