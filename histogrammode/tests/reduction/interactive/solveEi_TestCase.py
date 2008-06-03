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


import unittestX as unittest


class TestCase(unittest.TestCase):


    def test(self):
        """reduction.interactive: solveEi
        """
        import reduction.interactive as ri

        ri.getRun.select('arcs')
        r = ri.getRun('ARCS_279')
        print 'read Idpt'
        idpt = r.getIdpt( (3000,6000,10) )
        
        ri.solveEi.select('use elastic peaks')
        idpt = idpt[ (20,25), (), (), () ]
        
        print 'solve incident energy'
        ei = ri.solveEi( run = r, idpt = idpt )

        from reduction.units import energy
        expected= 99 * energy.meV 
        self.assertAlmostEqual( ei/expected, 1., places = 1 )
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
