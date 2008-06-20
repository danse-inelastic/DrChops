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



import unittest


from unittestX import TestCase as base
class TestCase(base):


    def test1(self):
        """SolidAngleCalculator
        """
        from reduction.core.ARCS.SolidAngleCalculator import SolidAngleCalculator
        calculator = SolidAngleCalculator()
        
        import numpy
        pixelpositions = numpy.array(
            [ [0,3.,0], [0,3,1], [3,0,0], [3,0,1], [0,0,0] ] )
        npixels = len(pixelpositions)
        
        #compute solid angles
        solidangles = numpy.zeros( npixels )
        cm = units.length.cm
        pixelradius = 1*cm
        pixelheight = 1*cm
        calculator(solidangles, pixelpositions, pixelradius, pixelheight)
        
        self.assert_( numpy.abs( solidangles[0] - 2.222e-5 ) < 1e-7 )
        self.assert_( numpy.abs( solidangles[1] - 2.222e-5* (3/numpy.sqrt(10.))**3 ) < 1e-7 )
        self.assert_( numpy.abs( solidangles[2] - solidangles[0] ) < 1e-10 )
        self.assert_( numpy.abs( solidangles[3] - solidangles[1] ) < 1e-10 )
        self.assert_( str(solidangles.mean()) != 'nan' )
        return
        
            
    pass # end of TestCase


import reduction.units as units


import unittest

def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    journal.debug('reduction.core.getPixelInfo' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
