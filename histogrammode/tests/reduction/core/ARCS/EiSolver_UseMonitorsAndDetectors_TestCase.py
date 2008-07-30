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


import os
datadir = '384'


import unittest

from unittestX import TestCase as base
class TestCase(base):

    
    def _test1(self):
        """reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors: getTofCentersAndDistances_Monitors
        """
        import histogram.hdf as hh
        m1itof = hh.load( os.path.join( datadir, 'm1itof.h5'), 'I(tof)')
        m2itof = hh.load( os.path.join( datadir, 'm2itof.h5'), 'I(tof)')
        itofs = [m1itof, m2itof]

        from reduction import units

        from arcseventdata import getinstrumentinfo
        ii = getinstrumentinfo( 'ARCS.xml' )
        dists = [
            ii[ 'moderator-monitor1 distance' ] * units.length.meter,
            ii[ 'moderator-monitor2 distance' ] * units.length.meter,
            ]

        ei_nominal = 30
        from reduction.utils import conversion as C
        velocity_guess = C.e2v( ei_nominal ) * units.length.meter / units.time.second
        from reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors import getTofCentersAndDistances_Monitors
        centers, dists = getTofCentersAndDistances_Monitors( itofs, dists, velocity_guess )
        self.assertEqual( len(centers) , 2 ) 
        self.assertEqual( len(dists) , 2 )
        return


    def _test2(self):
        """reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors: getTofCenter_vs_Distance_Pixels
        """
        import histogram.hdf as hh
        ipdpt = hh.load( '384/ipdpt.h5', 'I(pdpt)' )

        from reduction.core.ARCS import EiSolver_UseMonitorsAndDetectors as S
        ipt = S.getipt( ipdpt )
        centers = S.getTofCenters_UniquePixels( ipt )

        import arcseventdata as aed
        dists_hist = aed.getinstrumentinfo('ARCS.xml')[ 'dists' ]
        dists = S.getDistances_UniquePixels( dists_hist )

        centers, dists = S.sortTofCentersAndDistance_Pixels( centers, dists )
        centers, dists = S.removeBadPoints_TofCentersAndDistance_Pixels( centers, dists )
        import histogram as H
        h = H.histogram( 'h', [ ('x', dists, 'meter') ], data = centers, unit = 'second' )
        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( h )
        return


    def _test2a(self):
        """reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors: getTofCenter_vs_Distance_Pixels
        """
        import histogram.hdf as hh
        ipdpt = hh.load( '384/ipdpt.h5', 'I(pdpt)' )

        from reduction.core.ARCS import EiSolver_UseMonitorsAndDetectors as S
        ipt = S.getipt( ipdpt )
        centers = S.getTofCenters_UniquePixels( ipt )

        import arcseventdata as aed
        dists_hist = aed.getinstrumentinfo('ARCS.xml')[ 'dists' ]
        dists = S.getDistances_UniquePixels( dists_hist )

        centers, dists = S.sortTofCentersAndDistance_Pixels( centers, dists )
        import histogram as H
        h = H.histogram( 'h', [ ('x', dists, 'meter') ], data = centers, unit = 'second' )
        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( h )
        return


    def _test2b(self):
        """reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors: getTofCenter_vs_Distance_Pixels
        """
        import histogram.hdf as hh
        ipdpt = hh.load( '384/ipdpt.h5', 'I(pdpt)' )

        from reduction.core.ARCS import EiSolver_UseMonitorsAndDetectors as S
        ipt = S.getipt( ipdpt )
        centers = S.getTofCenters_UniquePixels( ipt )

        import arcseventdata as aed
        dists_hist = aed.getinstrumentinfo('ARCS.xml')[ 'dists' ]
        dists = S.getDistances_UniquePixels( dists_hist )

        centers, dists = S.removeBadPoints_TofCentersAndDistance_Pixels( centers, dists )
        return

    
    def _test3(self):
        """reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors: getTofCenter_vs_Distance
        """
        #distances and tof centers for unique pixels
        
        import histogram.hdf as hh
        ipdpt = hh.load( '384/ipdpt.h5', 'I(pdpt)' )

        from reduction.core.ARCS import EiSolver_UseMonitorsAndDetectors as S
        ipt = S.getipt( ipdpt )
        pixeltofs = S.getTofCenters_UniquePixels( ipt )

        import arcseventdata as aed
        dists_hist = aed.getinstrumentinfo('ARCS.xml')[ 'dists' ]
        pixeldists = S.getDistances_UniquePixels( dists_hist )
        
        pixeltofs, pixeldists = S.removeBadPoints_TofCentersAndDistance_Pixels( pixeltofs, pixeldists )

        # distances and tof centers for monitors
        import histogram.hdf as hh
        m1itof = hh.load( os.path.join( datadir, 'm1itof.h5'), 'I(tof)')
        m2itof = hh.load( os.path.join( datadir, 'm2itof.h5'), 'I(tof)')
        itofs = [m1itof, m2itof]

        from reduction import units

        from arcseventdata import getinstrumentinfo
        ii = getinstrumentinfo( 'ARCS.xml' )
        dists = [
            ii[ 'moderator-monitor1 distance' ] * units.length.meter,
            ii[ 'moderator-monitor2 distance' ] * units.length.meter,
            ]

        ei_nominal = 30
        from reduction.utils import conversion as C
        velocity_guess = C.e2v( ei_nominal ) * units.length.meter / units.time.second
        from reduction.core.ARCS.EiSolver_UseMonitorsAndDetectors import getTofCentersAndDistances_Monitors
        mtofs, mdists = getTofCentersAndDistances_Monitors( itofs, dists, velocity_guess )

        mod2sample = ii['moderator-sample distance']

        dists = list(pixeldists + mod2sample) + list(mdists) 
        centers = list(pixeltofs) + list( mtofs )

        import pickle
        pickle.dump( (pixeldists, pixeltofs, mdists, mtofs, dists, centers),
                     open('tmp.pkl','w') )

        centers, dists = S.sortTofCentersAndDistance_Pixels( centers, dists )
        
        import histogram as H
        h = H.histogram( 'h', [ ('x', dists, 'meter') ], data = centers, unit = 'second' )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( h )
        pickle.dump( h, open('tvsd.pkl', 'w'))
        return


    def test4(self):
        import histogram.hdf as hh
        ipdpt = hh.load( os.path.join( datadir, 'ipdpt.h5'), 'I(pdpt)' )
        m1itof = hh.load( os.path.join( datadir, 'm1itof.h5'), 'I(tof)')
        m2itof = hh.load( os.path.join( datadir, 'm2itof.h5'), 'I(tof)')
        mitofs = [m1itof, m2itof]
        eiguess = 30
        from reduction.core.ARCS import EiSolver_UseMonitorsAndDetectors as S
        h = S.getTvsD( ipdpt, mitofs, eiguess)

        from reduction.histCompat.PolynomialFitter import PolynomialFitter
        emission_time, reversed_velocity = PolynomialFitter(1).fit( h )
        velocity = 1./reversed_velocity
        print velocity, emission_time

        fitted = h.distance * reversed_velocity + emission_time
        import pylab
        #pylab.plot( h.distance, h.I )
        #pylab.plot( h.distance, fitted )
        #pylab.show()

        # remove outliers
        #h2 = h.copy()
        X = []
        Y = []
        YE2 = []
        for x,y1,y2 in zip( h.distance, h.I, fitted ):
            if abs(y1-y2)/y1 < 0.005:
                X.append(x)
                Y.append(y1)
                if x < 13: e2 = 1e-6
                elif x > 18: e2 = 2e-6
                else: e2 = 50e-6
                YE2.append(e2)
            continue
        import histogram as H
        h2 = H.histogram( 'tof', [ ('distance', X) ], data = Y, errors = YE2 )
        def linear(x, a0, a1): return a0+a1*x
        constraints = [
            (emission_time*0.95, emission_time*1.05),
            (reversed_velocity*0.95, reversed_velocity *1.05),
            ]
        from reduction.histCompat.Fit1DFunction import Fit1DFunction, minimizer
        class _:
            def plot(*args,**kwds): return
        fitter = Fit1DFunction( linear, minimizer = minimizer( tolerance = 1e-8 ), plotter = _() )
        emission_time2, reversed_velocity2 = fitter(h2, constraints )
        fitted2 = h2.distance * reversed_velocity2 + emission_time2
        pylab.plot( h2.distance, h2.I )
        pylab.plot( h2.distance, fitted2 )
        pylab.show()
        
        return
    
    pass # end of TestCase


import reduction.units as units


import unittest

def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    #journal.debug('reduction.core.getPixelInfo' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
