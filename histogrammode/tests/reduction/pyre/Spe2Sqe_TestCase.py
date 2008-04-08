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


import unittest

from pyre.applications.Script import Script

from unittestX import TestCase
class Spe2Sqe_TestCase(TestCase):


    from reduction.pyre.Spe2Sqe import Spe2Sqe
    

    def test(self):
        """
        """
        testFacility = self
        
        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory as inv
                spe2Sqe = inv.facility( 'spe2Sqe', factory = self.Spe2Sqe )
                pass #


            def main(self):
                #prepare data
                from histogram import axis, histogram, arange, datasetFromFunction
                phiAxis = axis( 'phi', arange( 0.5, 120.5, 1. ), unit = 'degree'  )
                EAxis = axis( 'energy', arange( -50, 50, 1.), unit='meV' )
                axes = phiAxis, EAxis
                spe = histogram('spe', axes )
                def f(phi): return 1+0.*phi
                spe[ (), 0. ] = datasetFromFunction(f, (phiAxis,)), datasetFromFunction(f, (phiAxis,))

                spe2Sqe = self.inventory.spe2Sqe

                sqe = spe2Sqe( 60.*meV, spe )
                
                #compare reduced data to direct computatiion
                self._check(sqe)
                return


            def _check(self, sqe):
                return
            
            
            def _defaults(self):
                Script._defaults(self)
                si = self.inventory
                spe2Sqe = si.spe2Sqe
                return


            def _configure(self):
                self._debug.log("_configure")
                Script._configure(self)
                si = self.inventory
                self.spe2Sqe = si.spe2Sqe
                return

            pass #
        
        t = Test('Spe2Sqe_TestCase')
        t.run()
        return
    
    pass # end of Spe2Sqe_TestCase


from pyre.units.energy import meV
    

import unittest

def pysuite():
    suite1 = unittest.makeSuite(Spe2Sqe_TestCase)
    return unittest.TestSuite( (suite1,) )


import journal
##     journal.debug('vectorCompat.ERebinAllInOne').activate()
##     journal.debug('Rebinner').activate()
journal.debug('Spe2Sqe_TestCase').activate()
journal.debug('Spe2Sqe').activate()
#journal.debug("NdArrayDataset").activate()

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Spe2Sqe_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
