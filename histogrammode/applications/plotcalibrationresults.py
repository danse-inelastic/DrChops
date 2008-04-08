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



def _plot( calibresutls ):
    X, Ys = calibresutls
    xname, x = X
    n = len(Ys)
    import math as m
    ncol = int( m.ceil( m.sqrt(n*1.0) ) )
    nrow = int( m.ceil(1.0*n/ncol))
    import pylab
    pylab.clf()
    for plotnum in range( n ):
        pylab.subplot(ncol, nrow, plotnum+1)
        yname, y = Ys[ plotnum ]
        pylab.plot( x, y )
        pylab.xlabel( xname )
        pylab.ylabel( yname )
        continue
    pylab.show()
    return



def main():
    import sys
    filename = sys.argv[1]
    import pickle
    c = pickle.load( open(filename) )
    _plot(c )
    return
    
    
if __name__ == "__main__": main()
    
    
# version
__id__ = "$Id$"

# End of file 
