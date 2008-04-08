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


from unittestX import TestCase
class getPixelInfo_TestCase(TestCase):


    def test1(self):
        """getPixelInfo: getDetectorAxesInfo
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'inputs/ARCS-partial.xml' )
        from reduction.core.getPixelInfo import getDetectorAxesInfo
        detaxes = getDetectorAxesInfo( instrument )
        print detaxes
        return
        
            
    def test2(self):
        """getPixelInfo: getPixelGeometricInfo
        """
        from instrument.nixml import parse_file
        instrument = parse_file( 'inputs/ARCS-partial.xml' )
        from reduction.core.getPixelInfo import getPixelGeometricInfo,\
             getDetectorAxes

        detaxes = getDetectorAxes( instrument )
        
        getPixelGeometricInfo( instrument, instrument.geometer,
                               detaxes )
        return
        
            
    pass # end of getPixelInfo_TestCase




import unittest

def pysuite():
    suite1 = unittest.makeSuite(getPixelInfo_TestCase)
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
__id__ = "$Id: getPixelInfo_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
