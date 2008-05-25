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


from reduction.interactive import idpt2sqe, getRun
import reduction.units as units
meV = units.energy.meV


class Idpt2Sqe_TestCase(unittest.TestCase):


    def test(self):
        """Idpt2Sqe
        """
        import os
        f = os.path.join( '..', '..', 'ins-data', 'Lrmecs', '4849' )
        run = getRun( f )
        
        instrument, geometer = run.getInstrument()
        Idpt = run.getIdpt()
        
        ei = 59.1 * meV
        sqehist = idpt2sqe(ei, Idpt, instrument, geometer)

        import pickle
        pickle.dump( sqehist, open('idpt2sqe-4849-sqe.pkl', 'w') )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( sqehist )
        raw_input( 'Press <ENTER> to continue' )
        return


    pass # end of TimeBG_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Idpt2Sqe_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
