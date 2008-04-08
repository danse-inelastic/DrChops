#!/usr/bin/env python

# read S(Q,E)
from cPickle import load
q,e,s,serr = load( open('sqe.pkl') )

positive_e = []
for item in e:
    if item>=0.0 : positive_e.append( item )
    continue

nEBins = len(positive_e)
s1 = s[ -nEBins:, :] # e>0 part of S(Q,E)
serr1 = serr[ -nEBins:, :]
#print s1

# sum over q indexes
import numpy as N
s_e = N.sum( s1, 1 )
s_e_err = N.sum( serr1, 1 )
print s_e

# array of phonon energy
phonon_e = N.array(positive_e, copy=1)

# function of 1/<n+1>
def reciThermo(phonon_e):
    import math
    ex = math.exp(phonon_e*11.605/300)
    return (ex-1)/ex

# density of states
reciThermoFactors = N.array( [ reciThermo(e) for e in phonon_e ] )
dos = s_e * phonon_e * reciThermoFactors
dos_err = s_e_err * phonon_e  * phonon_e * reciThermoFactors * reciThermoFactors

#save
from cPickle import dump
dump( (phonon_e, dos, dos_err), open('dos.pkl', 'w') )

# plot
import pylab
#pylab.plot( dos )
#pylab.plot( N.sqrt( dos_err ) )
pylab.errorbar( phonon_e, dos, yerr = N.sqrt(dos_err) )
pylab.show()
