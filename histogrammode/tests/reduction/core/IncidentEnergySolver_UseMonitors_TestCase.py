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


from reduction.core.IncidentEnergySolver_UseMonitors \
     import IncidentEnergySolver_UseMonitors as Solver, debug

import unittestX as unittest


from pyre.units.energy import meV

class IncidentEnergySolver_UseMonitors_TestCase(unittest.TestCase):


    def testLrmecs(self):
        from measurement.ins.LRMECS import createRun as  createLrmecsRun
        run = createLrmecsRun( '../../ins-data/Lrmecs/4849' )
        instrument, geometer = run.getInstrument()
        eiSolved = Solver(0,1)(run)
        self.assertAlmostEqual( 59.17, eiSolved/meV, 2 )
        return


    def test(self):
        """IncidentEnergySolver_UseMonitors
        """

        from TestRun_for_IncidentEnergySolverUsingMonitors import Run, ei as eiExpected
        run = Run()
        
        eiSolver = Solver(1,2)
        
        eiSolved = eiSolver( run )
        
        self.assertAlmostEqual( eiExpected, eiSolved/meV )
        return
    

    pass # end of IncidentEnergySolver_UseMonitors_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_UseMonitors_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    #debug.activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: IncidentEnergySolver_UseMonitors_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
