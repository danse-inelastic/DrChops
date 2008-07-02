


def peakcenter( itof, mod2monitor, velocityguess, monno, export ):
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
    


def run( guess = 70,  export = {} ):
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
    import histogram.hdf as hh
    m1 = hh.load( 'm1Itof.h5', 'I(tof)' )
    m2 = hh.load( 'm2Itof.h5', 'I(tof)' )
    export['m1'] = m1
    export['m2'] = m2
    from reduction.utils import conversion as C
    v = C.e2v( guess )
    from arcseventdata.getinstrumentinfo import getinstrumentinfo as gii
    arcs = gii('ARCS.xml')
    mod2m1 = arcs['moderator-monitor1 distance']
    mod2m2 = arcs['moderator-monitor2 distance']

    t1 = peakcenter( m1, mod2m1, v, 1, export )
    t2 = peakcenter( m2, mod2m2, v, 2, export )
    
    v = (mod2m2-mod2m1)/(t2-t1)*1e6
    
    Ei = C.v2e( v )
    export['Ei'] = Ei

    emission_time = t1 - mod2m1/v * 1e6
    export['emission_time'] = emission_time
    return 

