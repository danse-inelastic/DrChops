#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.utils.data_converters.mslice_spe_writer import test


import unittest


from unittestX import TestCase
class mslice_writer_TestCase(TestCase):

    def test1D(self):
        "mslice_spe_writer"
        test()
        return
        
    pass # end of mslice_writer_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(mslice_writer_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: mslice_writer_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
