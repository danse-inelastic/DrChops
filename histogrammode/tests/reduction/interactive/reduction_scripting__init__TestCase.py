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


from reduction.interactive import *
cm = units.length.cm
mm = units.length.mm
degree = units.angle.degree

import unittestX as unittest


class reduction_interactive__init__TestCase(unittest.TestCase):


    def test(self):
        """vanadiumPlate
        """
        vp = vanadiumPlate( height = 10*cm, width = 5*cm, darkAngle = 135*degree )
        return
    

    pass # end of reduction_interactive__init__TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(reduction_interactive__init__TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()
##     journal.debug('reduction_interactive__init_').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: reduction_interactive__init__TestCase.py 1265 2007-06-06 03:58:45Z linjiao $"

# End of file 
