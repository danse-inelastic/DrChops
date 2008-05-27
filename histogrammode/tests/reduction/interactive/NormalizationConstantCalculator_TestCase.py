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


from reduction.interactive import calcNorm
import reduction.units as units
microsecond = units.time.microsecond

import unittestX as unittest


class NormalizationConstantCalculator_TestCase(unittest.TestCase):


    def test(self):
        """NormalizationConstantCalculator
        """
        from TestRun_for_NormalizationConstantCalculator import Run, tofstep, ic

        run = Run()

        monitorId = 3
        tofStart = 4000 * microsecond
        tofEnd = 5000 * microsecond
        monitor_norm = ( (tofEnd-tofStart)/tofstep + 1) * monitorId
        
        calcNorm.select( 'use a monitor', monitorId = monitorId,
                         tofStart = tofStart, tofEnd = tofEnd )
        norm = calcNorm( run )
        self.assertAlmostEqual( monitor_norm, norm[0], 2 )

        calcNorm.select( 'use integrated moderator current' )
        norm = calcNorm( run )
        self.assertAlmostEqual( ic, norm[0], 2 )
        return
    

    pass # end of NormalizationConstantCalculator_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(NormalizationConstantCalculator_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##     journal.debug('NormalizationConstantCalculator').activate()
##     journal.debug('reduction.histCompat').activate()
##     journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
