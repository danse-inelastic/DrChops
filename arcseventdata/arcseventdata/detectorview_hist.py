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


def detectorview( Ipdp_ ):
    '''create a histogram that is just a view of the original Ipdpt
    The horizontal axis is 'detectorID', which actually includes
    both the packID (in a detector array, top, middle, or bottom)
    and the detectorID relative to its parent pack.
    The vertial axis is 'pixelID', which actually is a combination
    of pixelID and the axis of (top, middle, bottom).
    '''
    # this implemenation is pretty much a hack right now
    horizontal = 'super-detectorID'
    vertical = 'super-pixelID'
    
    import histogram as H
    view = H.histogram(
        'view',
        [ (horizontal, range(0, 39*8)),
          (vertical, range(0, 128*3)),
          ] + Ipdp_.axes()[ 3: ] )
    
    toppacks = range( 78, 116, 1 )
    for pack in toppacks:
        for tube in range(8):
            for pixel in range(128):
                view[ { horizontal: (pack-78)*8 + tube,
                        vertical: 383-pixel } ] =\
                      Ipdp_[ {'detectorpackID':pack,
                              'detectorID': tube,
                              'pixelID': pixel} ]

    middlepacks = range( 39, 78, 1 )
    for pack in middlepacks:
        for tube in range(8):
            for pixel in range(128):
                view[ {horizontal: (pack-39)*8 + tube,
                       vertical: 255-pixel} ]=\
                      Ipdp_[ {'detectorpackID':pack,
                              'detectorID': tube,
                              'pixelID': pixel} ]
                
    bottompacks = range( 1, 39, 1 )
    for pack in bottompacks:
        for tube in range(8):
            for pixel in range(128):
                view[ {horizontal: (pack-1)*8 + tube,
                       vertical: 127-pixel} ]=\
                      Ipdp_[ {'detectorpackID':pack,
                              'detectorID': tube,
                              'pixelID': pixel} ]

    return view



# version
__id__ = "$Id$"

#  End of file 
