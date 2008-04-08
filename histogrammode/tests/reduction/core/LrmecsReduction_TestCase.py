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


import unittestX as unittest


class LrmecsReduction_TestCase(unittest.TestCase):

    def test(self):
        "LRMECS reduction"
        filename = '../../ins-data/Lrmecs/4849'
        reduce( filename, 60, (5000,5500) )
        return

    pass # end of LrmecsReduction_TestCase


def reduce( filename, eiGuess, tbgWindow, mask = None ):
    if mask is None:
        from instrument import mask
        mask = mask()
        pass
    
    from measurement.ins.LRMECS import createRun as createLrmecsRun
    run = createLrmecsRun(filename)
    
    instrument, geometer = run.getInstrument()
    Idpt = run.getIdpt()

    from reduction.core.IncidentEnergySolver_UseMonitors import IncidentEnergySolver_UseMonitors as EiSolver
    from reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as TIBG
    from reduction.core.Idpt2Sqe import Idpt2Sqe

    TIBG( *tbgWindow )( Idpt )
    
    ei = EiSolver(0,1)(run)

    Idpt2Sqe()( ei, Idpt, instrument, geometer )

    return


    
def pysuite():
    suite1 = unittest.makeSuite(LrmecsReduction_TestCase)
    return unittest.TestSuite( (suite1,) )


def main():
    #debug.activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('LrmecsReduction').activate()
    journal.debug('reduction.histCompat').activate()
    journal.debug('eiSolver').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: LrmecsReduction_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 


