

def makeGaussianHistogram( ht = 10000, width = 1., center = 0.0 ):
    from histogram import histogram, axis, arange, datasetFromFunction

    xaxis = axis('x', arange( -10, 10, 0.1, 'd' ) )

    yh = histogram( 'y', [xaxis] )
    
    from numpy import exp, random, sqrt
    def f1(x):
        y = ht*exp( -((x-center)/width)**2 )
        return y 

    n = xaxis.size()
    y = datasetFromFunction( f1, [xaxis] )
    dy = sqrt(random.uniform(0, abs(y)))
    yh[()] = y+dy, dy**2
    return yh
