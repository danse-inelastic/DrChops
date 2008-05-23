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


from reduction.interactive import redcmds


import unittestX as unittest


class redcmds_TestCase(unittest.TestCase):


    def test(self):
        """reduction.interactive: redcmds
        """
        from reduction.interactive import redcmds
        redcmds()
        return
    

    pass # end of redcmds_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(redcmds_TestCase)
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
__id__ = "$Id: redcmds_TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
