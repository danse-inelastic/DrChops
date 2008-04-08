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


from reduction.pyre.preprocessors.IncidentEnergySolver_UseElasticPeaks import IncidentEnergySolver_UseElasticPeaks as Solver

from pyre.applications.Script import Script


import unittest


from unittestX import TestCase
class IncidentEnergySolver_UseElasticPeaks_Pharos_TestCase(TestCase):

    def test(self):
        """
        """
        testFacility = self

        dir =  "../../../ins-data/Pharos"
        from os.path import join
        datafile = join(dir, "Pharos_342.nx.h5")
        instrfile = join(dir, "PharosDefinitions.txt" )

        #create a pyre script to run the test
        class Test(Script):

            class Inventory(Script.Inventory):
                import pyre.inventory as inv
                eiSolver = inv.facility("eiSolver", factory = Solver)
                pass # end of Inventory

            def main(self):
                from measurement.ins.Pharos import createRun
                run = createRun( instrfile, datafile )
                es = self.eiSolver
                es.setInput('run', run)
                eiSolved = es.getOutput( 'Ei' )

                from reduction.units import energy
                eiExpected = 75.01*energy.meV
                testFacility.assertAlmostEqual( eiSolved/eiExpected, 1., 2)
                return

            def _defaults(self):
                eiSolver = self.inventory.eiSolver
                eiSolver.inventory.detectorSlice = "(100, 120), ()"
                return
            
            def _configure(self):
                si = self.inventory
                self.eiSolver = si.eiSolver
                return

            pass # end of Test
        t = Test('t')
        t.run()
        return
    

    pass # end of IncidentEnergySolver_UseElasticPeaks_Pharos_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(IncidentEnergySolver_UseElasticPeaks_Pharos_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
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
__id__ = "$Id: IncidentEnergySolver_UseElasticPeaks_Pharos_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
