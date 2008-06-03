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
from reduction.units import energy
meV = energy.meV

import unittestX as unittest


class TestCase(unittest.TestCase):


    def test(self):
        """reduction.interactive: idpt2spe
        """
        import reduction.interactive as ri

        ri.getRun.select('arcs')
        r = ri.getRun('ARCS_279')
        print 'read Idpt'
        idpt = r.getIdpt( (3000,6000,10) )

        ei = 99.3 * meV
        instrument, geometer = r.getInstrument()

        print 'idpt to spe'
        spe = ri.idpt2spe( ei, idpt, instrument, geometer )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spe )
        return
    

    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
##     journal.debug('redcmds').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
