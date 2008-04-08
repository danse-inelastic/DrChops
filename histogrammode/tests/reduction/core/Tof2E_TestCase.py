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

debug = journal.debug( "Tof2E_TestCase" )
warning = journal.warning( "Tof2E_TestCase" )


from pyre.units.length import mm, meter
from pyre.units.energy import meV
from pyre.units.time import microsecond, second


class Tof2E_TestCase(unittest.TestCase):


    Tof2E = None # overload this to test different subclasses
     
    def test(self):
        "Tof2E"
        ei = 60 *meV
        nDets = 200
        mod2sampleDistance = 10000. * mm
        from reduction.utils.conversion import e2v
        velocity = e2v( ei/meV ) * meter/second
        
        #inputs
        print "Creating inputs"
        from histogram import histogram, axis, datasetFromFunction, arange
        detIDaxis = axis( 'detID', range(0,nDets) )
        
        distances = histogram( 'distances', [detIDaxis], unit = 'mm' )

        R = 1000. * mm
        def d(detID): return (detID * R/1000 + R)/mm
        distances[()] = datasetFromFunction(d, [detIDaxis] ) * mm, 0 * mm * mm

        tof1 = (mod2sampleDistance) / velocity 
        tof2 = (mod2sampleDistance + 2*R) / velocity 
        tofAxis = axis(
            'tof',
            arange(tof1/microsecond, tof2/microsecond, 10.),
            unit='microsecond')
        

        #make input histogram
        print "Creating input histogram"
        inHist = histogram( 'I(tof)', [detIDaxis, tofAxis] )

        for detID in detIDaxis.binCenters():
            dist = distances[ detID][0]
            tof = (mod2sampleDistance + dist) / velocity /microsecond

            from reduction.core.numeric_functors import Gaussian
            g = Gaussian( tof, 1000., (tof2-tof1)/microsecond/200. )
            inHist[ detID, () ] = datasetFromFunction( g, [tofAxis] ), None
            debug.log( "detID = %s, dist = %s, tof=%s, tof1= %s, tof2 = %s" % (
                detID, dist, tof, tof1, tof2) )
            debug.log( "I(tof) = %s" % (
                inHist[detID,()].data().storage().asList(), ) )
            continue

        # output histogram
        EAxis = axis( 'energy', arange( 40, 80, 1.), unit = 'meV')
        outHist = histogram('I(E)', [detIDaxis, EAxis] )
        
        # tof --> E
        print "Converting I(tof) --> I(E)"
        Tof2E = self.Tof2E( )
        distances += mod2sampleDistance, 0.0 * mm * mm
        Tof2E(inHist, outHist, distances )

        
        # check
        print "Check conversion results"
        for detID in detIDaxis.binCenters():
            debug.log( "I(E) = %s" % (
                outHist[detID, ()].data().storage().asList(), ) )
            for e in EAxis.binCenters():
                v = outHist[ detID, e ][0]
                debug.log( "detID %s, e %s: v = %s" % (
                    detID, e, v) )
                e *= EAxis.unit()
                if abs(e-ei)/ei < 1e-5:
                    self.assert_( v > 10 )
                    pass
                else:
                    self.assertAlmostEqual( v, 0, places = 2 )
                    if abs(v) > 1e-5:
                        debug.log( "detID %s, e %s: %s is not zero" % (
                            detID, e, v) )
                    pass
                continue
            continue
        return 
        
        
    pass  # end of Tof2E_TestCase


class TestDefaultImpl( Tof2E_TestCase ):

    from reduction.core.Tof2E import Tof2E

    pass # end of TestDefaultImpl
     
    
def pysuite():
    suite1 = unittest.makeSuite(TestDefaultImpl)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    #from reduction.core.Tof2E import debug
    #debug.activate()

    journal.debug('EBinCalcor').activate()
    
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
