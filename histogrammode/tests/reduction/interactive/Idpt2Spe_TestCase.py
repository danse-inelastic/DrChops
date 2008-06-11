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


from reduction.interactive import idpt2spe, getRun
import reduction.units as units
meV = units.energy.meV


class Idpt2Spe_TestCase(unittest.TestCase):


    def test(self):
        """Idpt2Spe
        """
        import os
        f = os.path.join( '..', '..', 'ins-data', 'Lrmecs', '4849' )
        getRun.select('lrmecs')
        run = getRun( f )
        
        instrument, geometer = run.getInstrument()
        Idpt = run.getIdpt()
        
        ei = 59.1 * meV
        spehist = idpt2spe(ei, Idpt, instrument, geometer)

        import pickle
        pickle.dump( spehist, open('idpt2spe-4849-spe.pkl', 'w') )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spehist )
        raw_input( 'Press <ENTER> to continue' )
        return


    def test2(self):
        """Idpt2Spe(ei, idpt, run)
        """
        import os
        f = os.path.join( '..', '..', 'ins-data', 'Lrmecs', '4849' )
        getRun.select('lrmecs')
        run = getRun( f )
        
        Idpt = run.getIdpt()
        
        ei = 59.1 * meV
        spehist = idpt2spe(ei, Idpt, run = run)

        import pickle
        pickle.dump( spehist, open('idpt2spe2-4849-spe.pkl', 'w') )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spehist )
        raw_input( 'Press <ENTER> to continue' )
        return


    pass # end of TimeBG_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Idpt2Spe_TestCase)
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
