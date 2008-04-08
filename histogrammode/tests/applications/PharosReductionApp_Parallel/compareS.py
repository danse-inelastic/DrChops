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
    q,e,s,serr = load( open(f) )
    q1,e1,s1,serr1 = load( open(f1) )

    import pylab
    pylab.clf()
    pylab.subplot(121)
    plot( q,e,s, min = 0, max = guessMax(s) )
    pylab.subplot(122)
    plot(q1,e1,s1, min = 0, max = guessMax(s1) )
    pylab.show()
    yes = raw_input( "Does the two plots look similar? (y/n) " )
    if yes != 'y': raise "%s is not what we expect!" % name 
    return



def plot(x, y, z, min = None, max = None):
    from reduction.utils.plotter import pylabPlotter2D as pl
    pl.plot_(x,y,z, min = min, max = max)
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
