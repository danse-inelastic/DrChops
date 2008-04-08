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
import journal

debug = journal.debug( "ApplyMaskToHistogram_TestCase" )


from reduction.core.ApplyMaskToHistogram import applyMask


class ApplyMaskToHistogram_TestCase(unittest.TestCase):
     
    def test(self):
        "ApplyMaskToHistogram"
        from histogram import *
        h = histogram( 'h',
                       [ ('detectorID', [1,2,3]),
                         ('pixelID', [4,5,6,7] ) ] )
        def f(detID, pixID): return detID + pixID
        detectorIDaxis = h.axisFromName( 'detectorID' )
        pixelIDaxis = h.axisFromName( 'pixelID' )
        h[(),()] = datasetFromFunction( f, (detectorIDaxis, pixelIDaxis) ), \
                   datasetFromFunction( f, (detectorIDaxis, pixelIDaxis) )
        print h.data().storage().asList()

        from instrument.DetectorMask import DetectorMask
        mask = DetectorMask([1], [4], [(3,6)])

        applyMask( mask, h )

        self.assertVectorAlmostEqual(
            h.data().storage().asList(),
            [0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 8.0, 9.0, 0.0, 8.0, 0.0, 10.0] )
        return 
        
        
    pass  # end of ApplyMaskToHistogram_TestCase
     
    
def pysuite():
    suite1 = unittest.makeSuite(ApplyMaskToHistogram_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    #from reduction.core.ApplyMaskToHistogram import debug
    #debug.activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
