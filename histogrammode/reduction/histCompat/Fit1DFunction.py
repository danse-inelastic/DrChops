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


import journal
jrnltag = 'Fit1DFunction'
debug = journal.debug( jrnltag )


def fit1DGaussian( histogram, box=None, tolerance = 0.001, errors_as_weights = True):
    '''fit y(x) curve to

  a[0] + a[1] * exp( -((x-a[2])/a[3]) ** 2 )

Inputs:

  histogram: 1D histogram y(x)
  box: box constraints of parameters
  errors_as_weights: use error bars as weights of fitting
  '''

    if box is None:
        box = _guessBoxForGaussian( histogram )
        debug.log( 'guessed bound box: %s' % (box,) )
        pass

    m = minimizer( tolerance = tolerance )

    fit = Fit1DFunction( Gaussian, minimizer = m )

    return fit( histogram, box, errors_as_weights = errors_as_weights)

from functors import Gaussian
fit1DGaussian.functor = Gaussian



import numpy


class Fit1DFunction( object):
    
    """Fit f(x) function to data"""

    def __call__( self, histogram, box, errors_as_weights = True):
        '''fit histogram y(x) to a function

        histogram: 1D y(x) curve
        box: box constraints of parameters of the function to fit
        errors_as_weights: use error bars as weights of fitting
        '''
        axes = histogram.axes()
        assert len(axes) == 1, "Cannot deal with multi-dimensional data: "\
               "axes = %s" % (axes,)
        xaxis = axes[0]
        x = xaxis.binCenters()
        y = histogram.data().storage().asNumarray()

        if errors_as_weights:
            yerr2 = histogram.errors().storage().asNumarray().copy()
            assert (yerr2 >= 0).all(), "error bar must be not negative"
            if 0. in yerr2:
                # positive values in error bars
                nonzeros = yerr2[ yerr2 > 0 ]

                if len(nonzeros) == 0:
                    # all error bars are zero
                    raise ValueError, \
                          "error bar are all zero! "\
                          "Weights would be all NaN.\n"
                
                # add a tiny positive number to error bar?
                min = numpy.min( nonzeros )
                yerr2 += min
                pass
            
            weights = 1/numpy.sqrt(yerr2)
        else:
            weights = numpy.ones( len( y ) )

        #print x,y, weights
        engine = self._engine

        ret = engine( x, y, weights, box )

        return ret


    def __init__( self, functor,
                  minimizer = None, plotter = None):
        from reduction.vectorCompat.Fit1DFunction import Fit1DFunction
        self._engine = Fit1DFunction( functor, minimizer = minimizer,
                                      plotter = plotter )
        return


    pass # end of Fit1DFunction


from reduction.vectorCompat.MinimizeFunction import minimizer



def _guessBoxForGaussian( histogram ):
    '''guess the bound box paramerters of a gaussian for
    the given curve.

    The gaussian functor to fit is given in module "functors".
    '''
    x = histogram.axes()[0].binCenters()
    y = histogram.data().storage().asNumarray()
    n = len(y)
    m = n/10
    #assume the peak is in the center of the curve
    #so the points around begining and ending are background
    #points.
    bg = (sum(y[:m]) + sum(y[-m:]) )/2./m
    ymin = min(y); ymax = max(y)
    
    #peak is assuemd to be in the center of the curve,
    #so we can guess the y value of the peak
    #by taking average around center area.
    peakave = sum( y[ 4*m: 6*m ] )/ 2/m

    if peakave > bg :
        # this means the peak is pointing up
        h = ymax-bg
        # h is positive
        hrange = h/2, h*2
    else:
        # this means the peak is pointing down
        h = ymin - bg
        # h is negative
        hrange = h*2, h/2

    Dx = x[-1] - x[0]

    return [ (bg/10, bg*3), # bg
             hrange,  # height
             (x[0] + Dx/3, x[-1] - Dx/3), # center
             (Dx/10, Dx/2) # width
             ]


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

    from histogram import histogram, axis
    xaxis = axis( 'x', expx )
    yhist = histogram( 'y(x)', [xaxis] )
    yhist[()] = expy, weights

    def f(x, a): return a*x*x

    fit = Fit1DFunction( f )

    assert  abs(fit( yhist, [ (0,2) ] )[0] -1) < 0.1

    return


def _makeGaussianHistogram( ht = 10000):
    from histogram import histogram, axis, arange, datasetFromFunction

    xaxis = axis('x', arange( -10, 10, 0.1, 'd' ) )

    yh = histogram( 'y', [xaxis] )
    
    from numpy import exp, random, ones, sqrt
    def f1(x):
        y = ht*exp( -x**2 )
        return y 

    n = xaxis.size()
    y = datasetFromFunction( f1, [xaxis] )
    dy = sqrt(random.uniform(0, abs(y)))
    yh[()] = y+dy, dy**2
    return yh


def test3():
    from numpy import exp
    def f(x, a, b, c): return a * exp( - ((x-b)/c)**2 )

    tolerance = 0.0001
    m = minimizer( tolerance = tolerance )
    
    fit = Fit1DFunction( f, minimizer = m )

    box = [
        (1000, 100000),
        (-1., 1.),
        (0.5, 1.5),
        ]
    yh = _makeGaussianHistogram()
    print fit( yh, box)

    return


def test4():
    yh = _makeGaussianHistogram()
    box = [
        (-1,1),
        (1000, 50000),
        (-1., 1.),
        (0.5, 1.5),
        ]
    print fit1DGaussian( yh, box )
    return


def test5():
    yh = _makeGaussianHistogram()
    print fit1DGaussian( yh )
    return


def test6():
    yh = _makeGaussianHistogram(-10000)
    print fit1DGaussian( yh )
    return


def test7():
    yh = _makeGaussianHistogram(-10000)
    yh.errors().storage().asNumarray()[ : ] = 0
    try:
        fit1DGaussian( yh )
    except ValueError:
        print "good. catch ValueError"
    else:
        raise "Did not catch a ValueError"

    fit1DGaussian( yh, errors_as_weights = False )
    return



def main():
    test1()
    test3()
    test4()
    test5()
    test6()
    test7()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
