#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def peakcenter_by_fitting_to_parabolic( itof, mod2monitor, velocityguess, monno, export ):
    t = mod2monitor/velocityguess * 1e6 # microsecond
    
    width = t/10
    
    pk = itof[ (t-width, t+width) ]
    export ['m%spk' % monno ] = pk

    from reduction.histCompat import findPeakPosition
    
    center = findPeakPosition( pk, n=8 )
    
    return center


def peakcenter_by_fitting_to_gaussian( itof, mod2monitor, velocityguess, monno, export ):
    t = mod2monitor/velocityguess * 1e6 # microsecond
    
    width = t/10
    
    pk = itof[ (t-width, t+width) ]
    export ['m%spk' % monno ] = pk

    from reduction.scripting import fitg1

    bg, ht, center, width = fitg1( pk )
    gaussian = fitg1.functor( bg, ht, center, width )
    
    import histogram as H
    export ['m%spkfit' % monno ] = H.histogram(
        'm%spkfit'% monno,
        [pk.axisFromName('tof')],
        fromfunction = gaussian )
    return center
    



def calcEi( m1Itof, m2Itof, guess = 70, find_peakcenter = None, export = {}):
    
    if find_peakcenter is None:
        find_peakcenter = peakcenter_by_fitting_to_parabolic

    # approximate velocity 
    from reduction.utils import conversion as C
    v = C.e2v( guess )

    # instrument details
    from arcseventdata import getinstrumentinfo as gii
    arcs = gii('ARCS.xml')
    mod2m1 = arcs['moderator-monitor1 distance']
    mod2m2 = arcs['moderator-monitor2 distance']

    # find peak centers
    t1 = find_peakcenter( m1Itof, mod2m1, v, 1, export )
    t2 = find_peakcenter( m2Itof, mod2m2, v, 2, export )
    print t1,t2

    tofaxis = m1Itof.axisFromName('tof')
    tofunit = tofaxis.unit()
    from reduction.interactive import units
    second = units.time.second
    scale = second / tofunit

    print scale
    print mod2m2, mod2m1, t2, t1
    v = (mod2m2-mod2m1)/(t2-t1)*scale
    print v
    
    Ei = C.v2e( v )
    export['Ei'] = Ei

    emission_time = t1*tofunit - mod2m1/v * second
    export['emission_time'] = emission_time
    return 

    
def run( exprun, guess = 70, export = {}, find_peakcenter = None ):
    '''calculate Ei

    inputs:
      - guess: your guess of incident energy
      - export: environment dictionary

    outputs:
      - m1: monitor 1 I(tof)
      - m2: monitor 2 I(tof)
      - Ei: incident energy
      - m1pk: monitor1 the peak of interest
      - m2pk: monitor2 the peak of interest
      - m1pkfit: fit to m1pk
      - m2pkfit: fit to m2pk
    '''
    
    if find_peakcenter is None:
        find_peakcenter = peakcenter_by_fitting_to_parabolic

    m1Itof = exprun.getMonitorItof( 1 )
    m2Itof = exprun.getMonitorItof( 2 )
    
    export['m1Itof'] = m1Itof
    export['m2Itof'] = m2Itof

    calcEi( m1Itof, m2Itof,
            guess = guess, find_peakcenter = find_peakcenter, export = export)
    return 



# version
__id__ = "$Id$"

#  End of file 
