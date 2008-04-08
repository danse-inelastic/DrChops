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


from reduction.pyre.inventory.properties.NumberList import NumberList


import unittest


from unittestX import TestCase
class NumberList_TestCase(TestCase):

    def test(self):
        """cast
        """
        import pyre.inventory.Inventory as pI
        
        class Inventory( pI.Inventory ):
            
            n = NumberList('n')

            pass # end of Inventory

        inv = Inventory("test")
        inv.n = "[]"
        self.assertVectorEqual( inv.n, [] )
        inv.n = "[1,2,3]"
        self.assertVectorEqual( inv.n, [1,2,3] )
        return
    

    pass # end of NumberList_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(NumberList_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: NumberList_TestCase.py 834 2006-03-03 14:39:02Z linjiao $"

# End of file 
