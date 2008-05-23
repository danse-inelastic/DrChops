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


from reduction.interactive import *


import unittestX as unittest


class LrmecsReduction_TestCase(unittest.TestCase):
    
    def _test(self):
        "LRMECS reduction"
        filename = '../../ins-data/Lrmecs/4849'
        reduce( filename, 60, (5000,5500) )
        return

    def test2(self):
        "LRMECS reduction"
        filename = '../../ins-data/Lrmecs/4849'
        vfilename = '../../ins-data/Lrmecs/4779'
        reduce2( filename,60, (5000,5500), None,
                 vfilename, 2, 10, 135 )
        return
        

    pass # end of LrmecsReduction_TestCase


def reduce( filename, eiGuess, tbgWindow, mask = None ):
    if mask is None:
        from instrument import mask
        mask = mask()
        pass

    getRun.select('lrmecs')
    run = getRun(filename, interpolateData = 1)
    
    instrument, geometer = run.getInstrument()
    Idpt = run.getDetPixTOFData()

    tbgMin, tbgMax = tbgWindow
    removeTIBG.reconstruct( tbgMin = tbgMin, tbgMax = tbgMax )

    removeTIBG( Idpt )

    solveEi.select( 'use monitors', monitor1Id = 0, monitor2Id=1)
    ei = solveEi(run)

    sqe = idpt2sqe( ei, Idpt, instrument, geometer )

    plot( sqe )

    raw_input( 'Press <ENTER> to continue' )
    return


def reduce2( filename,eiGuess, tbgWindow, mask,
             calibFilename, thickness, width, darkAngle ):
    if mask is None:
        from instrument import mask
        mask = mask()
        pass

    getRun.select('lrmecs')
    run = getRun(filename, interpolateData = 0)
    
    instrument, geometer = run.getInstrument()
    Idpt = run.getDetPixTOFData()

    tbgMin, tbgMax = tbgWindow
    removeTIBG.reconstruct( tbgMin = tbgMin, tbgMax = tbgMax )

    removeTIBG( Idpt )

    solveEi.select( 'use monitors', monitor1Id = 0, monitor2Id = 1)
    ei = solveEi(run)

    vRun = getRun(calibFilename, interpolateData = 1)
    instrument,geometer = vRun.getInstrument()
    vSample = vanadiumPlate( thickness, width )
    instrument.changeSample( vSample )
    geometer.register( vSample, (0,0,0), (0,0,darkAngle) )
    
    cc = getCC( vRun, ei )

    plot( cc )

    for detID in cc.axisFromName('detectorID').binCenters():
##         print detID
##         if detID < 0: continue
        Idpt[detID, (),() ] /= cc[detID]
        continue

    sqe = idpt2sqe( ei, Idpt, instrument, geometer )

    plot( sqe )

    raw_input( 'Press <ENTER> to continue' )
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


