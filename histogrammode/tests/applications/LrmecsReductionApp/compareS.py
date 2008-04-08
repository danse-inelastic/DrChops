#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                   (C) Copyright 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os

def compareS( f, f1, name = "S(Q,E)" ):
    from pickle import load
    h = load( open(f) )
    h1 = load( open(f1) )

    import pylab
    pylab.clf()
    pylab.subplot(121)
    plot( h )
    pylab.subplot(122)
    plot( h1 )
    #pylab.draw()
    pylab.show()
    yes = raw_input( "Does the two plots look similar? (y/n) " )
    if yes != 'y': raise "%s is not what we expect!" % name 
    return


def plot( hist ):
    from pylab import clip, meshgrid, pcolormesh as pm
    x = hist.axisFromId(1).binBoundaries().asNumarray().copy()
    y = hist.axisFromId(2).binBoundaries().asNumarray().copy()
    X, Y = meshgrid(x,y)
    z = hist.data().storage().asNumarray().copy().T
    z = z.copy()
    max = guessMax( z )
    pm( X, Y, clip(z, 0, max) )
    return


from histogram.data_plotter import _guessMax as guessMax


def main():
    import sys
    print sys.argv
    f, f1 = sys.argv[1:]
    compareS( f, f1 )
    return


if __name__ == '__main__': main()

# version
__id__ = "$Id: PharosReductionLight.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
