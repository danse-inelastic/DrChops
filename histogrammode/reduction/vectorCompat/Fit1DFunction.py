#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import numpy

class Fit1DFunction( object):
    """Fit f(x) function to data"""

    def __call__( self, xs, ys, weights, box):
        '''fit data y(x) with eights to a function

        xs, ys: y(x) curve
        weights: weight for each data point
        box: box constraints of parameters of the function to fit
        '''
        xs = numpy.array(xs)
        ys = numpy.array(ys)
        weights = numpy.array( weights )

        functor = self._functor
        def resids( p ):
            args = [xs] + list(p)
            y1s = apply( functor, args)
            return numpy.sum( weights * (ys-y1s)**2 )
        
        minimizer = self._minimizer
        
        ret = minimizer( resids, box )

        self._comparePlot( ret, (xs, ys) )
        return ret


    def __init__( self, functor, minimizer = None, plotter = None):
        self._functor = self._make_functor(functor)
        if minimizer is None:
            from MinimizeFunction import MinimizeFunction
            minimizer = MinimizeFunction()
            pass
        self._minimizer = minimizer

        if plotter is None:
            from histogram.data_plotter import pylabPlotter1D as pylabPlotter
            plotter = pylabPlotter
            pass
        self._plotter = plotter
        return


    def _make_functor(self, functor):
        '''create a functor that is more like a function.
    The functor that this class accept has a form like this:
    
      def f(x, *args): ...                 (A)
    
    The input functor could be just good, or it could be a
    real functor:

      class F:                             (B)
          def __init__(self, *args): ...
          def __call__(self, x): ...
          pass
      
    This function will convet functor of whatever forms
    to form (A).
    '''
        if not isfunction( functor ):
            #suppose functor is a functor class
            def f( x, *args, **kwds):
                return functor(*args, **kwds)( x )
            return f
        return functor


    def _comparePlot(self, params, curvedata):
        functor = self._functor
        x, y = curvedata
        args = [x] + params
        y1 = apply( functor, args )
        plotter = self._plotter
        plotter.plot( x,y, symbol = '+' )
        plotter.plot( x,y1 )
        raw_input('press <ENTER> to continue')
        return


    pass # end of Fit1DFunction



def fitParabolic( x,y, weights = None ):
    
    def f(x, a0, a1, a2): return a0+ a1*(x-a2)**2

    from numpy import ones
    if weights is None: weights = ones( len(x), 'd' )

    dy = max(y)-min(y)
    dx =( x[-1]-x[0] ) /2.
    a1g = dy/dx/dx
    box = [
        (min(y), max(y)),
        (-a1g, a1g),
        (x[0], x[-1])
        ]

    fit = Fit1DFunction( f )

    return fit( x, y, weights, box )
    
    

def dummpyPlotter( *args, **kwds): return



def isfunction(f):
    from types import FunctionType
    return isinstance( f, FunctionType )


def test1():
    from numpy import array, ones, arange, exp
    expx = arange( -10, 10, 1., 'd')
    expy = expx ** 2
    import random
    for i in range(len(expy) ):
        expy[i] += random.uniform(0, expx[i]/10.)
        continue
    n = len(expx)
    weights = ones( n, 'd' )

    def f(x, a): return a*x*x

    fit = Fit1DFunction( f )

    assert  abs(fit( expx, expy, weights, [ (0,2) ] )[0] -1) < 0.1

    return


def test2():
    from numpy import array, ones, arange, exp
    expx = arange( -10, 10, 0.1, 'd')
    expy = exp( -expx**2 )
    import random
    for i in range(len(expy) ):
        expy[i] += random.uniform(0, expy[i]/20.)
        continue
    n = len(expx)
    weights = ones( n, 'd' )

    def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

    fit = Fit1DFunction( f )

    box = [
        (0., 2.),
        (-1., 1.),
        (0.5, 1.5),
        ]
    print fit( expx, expy, weights, box)

    return


def test3():
    from numpy import array, ones, arange, exp
    expx = arange( -10, 10, 0.1, 'd')
    expy = exp( -expx**2 )
    import random
    for i in range(len(expy) ):
        expy[i] += random.uniform(0, expy[i]/20.)
        continue
    n = len(expx)
    weights = ones( n, 'd' )

    def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

    tolerance = 0.0001
    from MinimizeFunction import VTR, MinimizeFunction
    minimizer = MinimizeFunction( termination = VTR( tolerance ), maxiter = 100000 )
    fit = Fit1DFunction( f )

    box = [
        (0., 2.),
        (-1., 1.),
        (0.5, 1.5),
        ]
    print fit( expx, expy, weights, box)

    return


def test4():
    from numpy import array, ones, arange, exp
    expx = arange( -10, 10, 0.1, 'd')
    expy = expx ** 2
    import random
    for i in range(len(expy) ):
        expy[i] += random.uniform(0, expy[i]/20.)
        continue
    
    a0, a1, a2 = fitParabolic( expx, expy )

    assert abs(a0) < 0.05, "a0 should be around zero, got %s" % a0
    assert abs(a1-1)< 0.05, "a1 should be around 1, got %s" % a1
    assert abs(a2) < 0.05, "a2 should be around 0, got %s" % a2
    return


def main():
    test1()
    test2()
    test3()
    test4()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
