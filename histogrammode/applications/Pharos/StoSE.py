#!/usr/bin/env python

import numpy as N


# read S(Q,E) histogram
from reduction.utils.pickle import load
#sQEHist = load( open('sQEHist.pkl') )
q,e,s,serr = load( 'sqe.pkl') 

## # get q,e,s

## s = sQEHist.data().storage().asNumarray()
## serr = sQEHist.errors().storage().asNumarray()
## q = sQEHist.q().binCenters()
## e = sQEHist.energy().binCenters()
## s.shape = len(q), len(e)
## serr.shape = len(q), len(e)
## s = N.transpose(s)
## serr = N.transpose(serr)


#calculate s(E)
s_E = N.sum( s, 1 )
sigma2_E = N.sum( serr, 1 )
sigma_E = N.sqrt( sigma2_E )


#pylab.plot( e, s_E, '-', e, serr_E, '+')
#pylab.plot( e, s_E, '-', e, sigma_E, '+')
from histogram.data_plotter import defaultPlotter1D
defaultPlotter1D.errorbar( e, s_E, yerr = sigma_E )

raw_input('continue...')
