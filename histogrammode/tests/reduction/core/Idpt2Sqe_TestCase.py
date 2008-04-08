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

debug = journal.debug( "Idpt2Sqe_TestCase" )


from reduction.core.Idpt2Sqe import Idpt2Sqe


from FakeMeasurement import Measurement


class Idpt2Sqe_TestCase(unittest.TestCase):
     
    def testCtor(self):
        "Idpt2Sqe: ctor"
        reducer = Idpt2Sqe(  )
        return


    def _testReduce(self):
        "Idpt2Sqe: reduce"
        from FakeInstrument import main as getInstr, R, numpxls

        ei = 47.043 # v=3000m/s

        from histogram import axis, arange
        EAxis = axis('energy', arange(-45, 45, 1.), unit='meV')
        QAxis = axis('Q', arange(0.0, 13.0, 1.0), unit='angstrom**-1')

        reducer = Idpt2Sqe( )

        instrument, geometer = getInstr()
        measurement = Measurement( instrument, geometer)
        Idpt = measurement.getRun('main').getIdpt()
        
        sqehist = reducer(ei, Idpt, instrument, geometer,
                          QAxis = QAxis, EAxis = EAxis)

        import pickle
        pickle.dump( sqehist, open('simplesqereducer-sqe.pkl', 'w') )
        return

    
    def testReduce2(self):
        "Idpt2Sqe: reduce LRMECS data"

        import os
        f = os.path.join( curdir(), '..','..', 'ins-data', 'Lrmecs', '4849' )
        from measurement.ins.LRMECS import createRun as createLrmecsRun
        run = createLrmecsRun( f )
        
        instrument, geometer = run.getInstrument()
        Idpt = run.getIdpt()
        
        reducer = Idpt2Sqe( )

        from pyre.units.energy import meV
        ei = 59.1 * meV
        sqehist = reducer(ei, Idpt, instrument, geometer)

        import pickle
        pickle.dump( sqehist, open('idpt2sqe-4849-sqe.pkl', 'w') )
        
        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( sqehist )
        raw_input( 'Press <ENTER> to continue' )
        return

    pass 


def curdir():
    import os
    return os.path.dirname( __file__ )
     
    
def pysuite():
    suite1 = unittest.makeSuite(Idpt2Sqe_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    from reduction.core.Idpt2Sqe import debug
    #debug.activate()

    #journal.debug( "RDriver" ).activate();
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
