#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from reduction.histCompat.Rebinner import *
from histogram import axis, datasetFromFunction, histogram, arange


import unittest

from unittestX import TestCase
class Rebinner_TestCase(TestCase):


    def test_weightedAverage( self):
        "Rebinner: weightedAverage"
        neighbors = [
            (None, 1.0, 10.0, 1.0),
            (None, 2.0, 10.0, 1.0),
            (None, 3.0, 10.0, 1.0),
            ]
        ave = weightedAverage_useNormalJacobians( neighbors )
        
        self.assertVectorAlmostEqual( ave.asTuple(), (10.0,0) )
        return

    
    def test_findNeighbors( self ):
        "Rebinner: findNeighbors"
        Y = (0,0)
        inYList = [
            ((0,0.6), 10., 1.),
            ((0,-1), 10., 1.),
            ((0.9,0), 10., 1.),
            ((-0.8,0), 10., 1.),
            ((2,0), 1000., 1. ),
            ]
        DY = (1,1)
        DY2 = (0.2, 0.2)
        DY3 = (0.001, 0.001)
        nNeighbors = 4
        neighbors = findNeighbors(Y, inYList, DY, DY2, DY3, nNeighbors)
        self.assertAlmostEqual( neighbors[0][1], 0.6 )
        self.assertAlmostEqual( neighbors[1][1], 0.8 )
        return
    

    def test1D(self):
        "Rebinner: 1D, linear"
        
        #create axis x
        min = 0.; delta = 1.0; nBinsX = 4
        axisX = axis( 'x', unit = 'meter', centers = arange( 0., 4.0, 1.0 ) )

        #create input histogram
        inHist = histogram(name = 'in', axes = [axisX,])
        from numpy import array
        inHist[ () ] = array([1,1,1,1]), array([0,0,0,0])
                      
        #create axis y
        min = 0.; delta = 1.0; nBinsY = 2
        axisY = axis( 'y', unit = 'meter', centers = arange(0., 2.0, 1.0) )

        #create output histogram
        outHist = histogram( 'out', (axisY,) )

        #create mapper
        def mapper(X):
            #input is a tuple
            x, = X
            #
            return x/2.,

        Jacobians = inHist.copy()
        def v(x): return 0.*x + 0.5
        Jacobians[ () ] = datasetFromFunction( v, [axisX] ), None

        #call rebinner
        from reduction.histCompat.Rebinner import rebinner
        rebinner.rebin( inHist, outHist, mapper, Jacobians)

        #check output
        outdataNA = outHist.data().storage().asNumarray()
        print outdataNA
        self.assertVectorAlmostEqual( outdataNA, [2., 2.] )

        return
    
    def test2DTo1D(self):
        "Rebinner: 2D --> 1D"
        R = 30
        #create axis x
        axisX = axis( 'x', arange(0., R, 1.) )

        #create axis y
        axisY = axis( 'y', arange(0., R, 1.) )

        #create input histogram
        inHist = histogram('in',  [axisX,axisY])

        from numpy import array
        inHist[(), ()] =  array([[1]*R]*R), None

        #create axis r
        axisR = axis( 'r', arange(0, R * 1.42, 1.) )

        #create output histogram
        outHist = histogram( 'out', axes = [axisR,])


        #create mapper
        def mapper(X):
            x,y = X
            from math import sqrt
            return sqrt(x*x + y*y),


        #the 'Jacobians'
        def v(x,y):
            from numpy import sqrt
            return sqrt(x*x + y*y)
        Jacobians = inHist.copy()
        Jacobians[ (), () ] = datasetFromFunction( v, [axisX, axisY] ), None

        #call rebinner
        from reduction.histCompat.Rebinner import rebinner
        rebinner.rebin( inHist, outHist, mapper, Jacobians, InversedJacobains = True, epsilon = -1)

        #check output
        outdataNA = outHist.data().storage().asNumarray()
        #print outdataNA
        for r, v in enumerate(outdataNA):
            if r<10: continue
            from math import pi
            expected = r 
            assert abs(v-expected)/max(expected,v) < 0.2, "%s != %s" % (v, expected)
        return
    
    
    def test2DTo2D(self):
        "Rebinner: 2D --> 2D"
        R = 10
        #create axis x
        axisX = axis( 'x', arange(0., R, 1.) )

        #create axis y
        axisY = axis( 'y', arange(0., R, 1.) )

        #create input histogram
        inHist = histogram('in',  [axisX,axisY])

        def f(x,y): return x-y
        
        inHist[(), ()] = datasetFromFunction( f, [axisX, axisY]), None

        #create axis x1
        axisX1 = axis( 'x1', arange(0., R, 1.) )

        #create axis y1
        axisY1 = axis( 'y1', arange(0., R, 1.) )
        
        #create output histogram
        outHist = histogram('out',  [axisX1,axisY1])

        #create mapper
        def mapper(X):
            x,y = X
            return y,x

        #the Jacobians
        def J(x,y):
            return 0*x+1
        Jacobians = inHist.copy()
        Jacobians[ (), () ] = datasetFromFunction( J, [axisX, axisY] ), None

        #call rebinner
        from reduction.histCompat.Rebinner import rebinner
        rebinner.rebin( inHist, outHist, mapper, Jacobians)

        #check output
        for x in axisX1.binCenters():
            for y in axisY1.binCenters():
                self.assertEqual( outHist[x,y][0], y-x )
        return
    

    def test3DTo3D(self):
        "Rebinner: 3D --> 3D"
        R = 10

        #create input histogram
        axisX = axis( 'x', arange(0., R, 1.) )
        axisY = axis( 'y', arange(0., R, 1.) )
        axisZ = axis( 'z', arange(0., R, 1.) )
        inHist = histogram('in',  [axisX,axisY,axisZ])

        def f(x,y,z): return x+y+z
        
        inHist[(), (), ()] = datasetFromFunction( f, [axisX, axisY, axisZ]), None

        
        #create output histogram
        axisX1 = axis( 'x1', arange(0., R, 1.) )
        axisY1 = axis( 'y1', arange(0., R, 1.) )
        axisZ1 = axis( 'z1', arange(0., R, 1.) )
        outHist = histogram('out',  [axisX1,axisY1,axisZ1])

        #create mapper
        def mapper(X):
            x,y,z = X
            return z,y,x

        #the Jacobians
        def J(x,y,z):
            return 0*x+1
        Jacobians = inHist.copy()
        Jacobians[ (), (), () ] = datasetFromFunction( J, [axisX, axisY, axisZ] ), None

        #call rebinner
        from reduction.histCompat.Rebinner import rebinner
        rebinner.rebin( inHist, outHist, mapper, Jacobians)

        return
    
    def test4DTo4D(self):
        "Rebinner: 4D --> 4D"
        R = 5

        #create input histogram
        axisX = axis( 'x', arange(0., R, 1.) )
        axisY = axis( 'y', arange(0., R, 1.) )
        axisZ = axis( 'z', arange(0., R, 1.) )
        axisU = axis( 'u', arange(0., R, 1.) )
        inHist = histogram('in',  [axisX,axisY,axisZ,axisU])

        def f(x,y,z,u): return x+y+z+u
        
        inHist[(), (), (), ()] = datasetFromFunction( f, [axisX, axisY, axisZ, axisU]), None

        
        #create output histogram
        axisX1 = axis( 'x1', arange(0., R, 1.) )
        axisY1 = axis( 'y1', arange(0., R, 1.) )
        axisZ1 = axis( 'z1', arange(0., R, 1.) )
        axisU1 = axis( 'u1', arange(0., R, 1.) )
        outHist = histogram('out',  [axisX1,axisY1,axisZ1,axisU1])

        #create mapper
        def mapper(X):
            x,y,z,u = X
            return u,z,y,x

        #the Jacobians
        def J(x,y,z,u):
            return 0*x+1
        Jacobians = inHist.copy()
        Jacobians[(), (), (), ()] = datasetFromFunction( J, [axisX, axisY, axisZ, axisU] ), None

        #call rebinner
        from reduction.histCompat.Rebinner import rebinner
        rebinner.rebin( inHist, outHist, mapper, Jacobians)

        return

    pass # end of Rebinner_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(Rebinner_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    debug.activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Rebinner_TestCase.py 1269 2007-06-19 07:52:27Z linjiao $"

# End of file 
