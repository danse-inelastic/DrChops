#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



'''
calculates theoretical efficieny of detectors
'''


import journal
#journal.debug( 'he3deteffic' ).activate()
#journal.debug( 'He3DetEffic' ).activate()


bottompacks = range(1, 39)
middlepacks = range(39, 78)
toppacks = range(78, 116)


def deteff_hist( energy, ARCSxml = 'ARCS.xml' ):
    '''comnpute detector efficieny as a function of pack, detector, pixel
    The returned object is a histogram eff( pack, det, pixel )
    '''
    detaxes = getdetaxes( ARCSxml )
    tubeaxis, pixelaxis = detaxes[1:]
    from instrument.nixml import parse_file
    instrument = parse_file( ARCSxml )
    geometer = instrument.geometer
    bottom, middle, top = theoeff_bottom_middle_top(
        energy, tubeaxis, pixelaxis, instrument, geometer)

    if isAxis(energy): energyAxis = energy
    else: energyAxis = None
    
    axes = list(detaxes)
    if energyAxis: axes.append(energyAxis)
    
    import histogram
    result = histogram.histogram('theoretical detector efficiency', axes )
    for pack in bottompacks:
        result[ { 'detectorpackID': (bottompacks[0], bottompacks[-1]) } ].I[:] = bottom.I
    for pack in middlepacks:
        result[ { 'detectorpackID': (middlepacks[0], middlepacks[-1]) } ].I[:] = middle.I
    for pack in toppacks:
        result[ { 'detectorpackID': (toppacks[0], toppacks[-1]) } ].I[:] = top.I
    return result
    

def getdetaxes(ARCSxml):
    import arcseventdata as aed
    ii = aed.getinstrumentinfo( 'ARCS.xml' )
    detaxes = ii['detector axes']
    return detaxes
    

def theoeff_bottom_middle_top(
    energy, tubeaxis, pixelaxis, instrument, geometer ):

    if isAxis(energy): energyAxis = energy
    else: energyAxis = None
    
    ds = instrument.getDetectorSystem()

    bottom_eff = make_pack_eff_hist(
        'bottom packs theoretical efficiency', tubeaxis, pixelaxis,
        energyAxis=energyAxis)
    pack20 = ds.elementFromId( 20 )
    calc_pack_eff( bottom_eff, energy, pack20, instrument, geometer )

    middle_eff = make_pack_eff_hist(
        'middle packs theoretical efficiency', tubeaxis, pixelaxis,
        energyAxis=energyAxis)
    pack57 = ds.elementFromId( 57 )
    calc_pack_eff( middle_eff, energy, pack57, instrument, geometer )

    top_eff = make_pack_eff_hist(
        'top packs theoretical efficiency', tubeaxis, pixelaxis,
        energyAxis=energyAxis)
    pack94 = ds.elementFromId( 94 )
    calc_pack_eff( top_eff, energy, pack94, instrument, geometer )

    return bottom_eff, middle_eff, top_eff





def make_pack_eff_hist( name, tubeaxis, pixelaxis, energyAxis=None):
    axes = [ tubeaxis, pixelaxis ]
    if energyAxis: axes.append(energyAxis)
    from histogram import histogram
    return histogram(name, axes)



def calc_pack_eff( eff_hist, energy, pack, instrument, geometer ):
    '''calculate detector efficiency for a detector pack

    eff_hist: the histogram to hold the result. axes should be [...detaxes...] if energy is one number (with unit), or [...detaxes..., energy] if energy is an axis.
    energy: neutron energy (a number (with unit) or an axis)
    pack: detector pack data object
    instrument, geometer: 
    '''
    if isAxis(energy): energyAxis = energy
    else: energyAxis = None
    
    ds = instrument.getDetectorSystem()
    
    from reduction.histCompat.He3DetEffic import He3DetEffic
    from math import sqrt

    prefix = '%s/%s' % (ds.name, pack.name)
    
    for tube in pack:
        
        tube_id = tube.id()
        tube_name = tube.name
        pressure = tube.pressure()
        radius = tube.shape().radius
        
        for pixel in tube:
            pixel_id = pixel.id()
            pixel_name = pixel.name
            position = geometer.position(
                '%s/%s/%s' % (prefix, tube_name, pixel_name) )
            x,y,z = position
            costheta = sqrt( (x*x+y*y)/(x*x+y*y+z*z) )
            
            calcEff = He3DetEffic(
                radius = radius,
                pressure = pressure,
                costheta = costheta )

            slicing = {
                'detectorID': tube_id,
                'pixelID': pixel_id,
                }
            if energyAxis:
                calcEff(energyAxis, eff_hist[slicing])
            else:
                eff = calcEff( energy )
                eff_hist[slicing] = eff, 0

            continue

        continue

    return



def isAxis(candidate):
    from histogram.Axis import Axis
    return isinstance(candidate, Axis)



def test():
    import reduction.units as units
    meV = units.energy.meV
    energy = 70*meV
    ARCSxml = 'ARCS.xml'
    deteff = deteff_hist( energy, ARCSxml )
    return


def main():
    test()
    return


if __name__ == '__main__': main()
    
# version
__id__ = "$Id$"

# End of file 
