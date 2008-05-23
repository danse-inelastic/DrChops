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


from reduction.interactive import getRun


class GetExperimentalRun_TestCase(unittest.TestCase):


    def testLrmecs(self):
        """GetExperimentalRun: Lrmecs
        """
        getRun.select('lrmecs')
        getRun( '../../ins-data/Lrmecs/4849' )
        return


    def testPharos(self):
        """GetExperimentalRun: Pharos
        """
        getRun.select('pharos')
        getRun( '../../ins-data/Pharos/PharosDefinitions.txt',
                '../../ins-data/Pharos/Pharos_342.nx.h5')
        return

    pass # end of TimeBG_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(GetExperimentalRun_TestCase)
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
