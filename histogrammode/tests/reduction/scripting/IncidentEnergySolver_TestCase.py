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


import journal


from reduction.scripting import solveEi


import unittestX as unittest


class IncidentEnergySolver_TestCase(unittest.TestCase):


    def test(self):
        """IncidentEnergySolver
        """
        from TestRun_for_IncidentEnergySolverUsingElasticPeaks import *

        solveEi.select( 'use elastic peaks' )
        run = Run()
        eiSolved = solveEi( run )
        
        self.assertAlmostEqual( ei, eiSolved, 3 )
        return
    

    pass # end of IncidentEnergySolver_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##     journal.debug('IncidentEnergySolver').activate()
##     journal.debug('reduction.histCompat').activate()
##     journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: IncidentEnergySolver_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
