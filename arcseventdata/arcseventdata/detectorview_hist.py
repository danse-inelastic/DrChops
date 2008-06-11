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

'''
super indexes:
  super_tubeid: roughly packid*8 + tubeid for each row of detectors
  super_pixelid: from 0 -> 127 * 3
'''


npixelspertube = 128
ntubesperpack = 8
nrows = 3
# pack id for the first pack in each row
startpacks = {
    0: 1,
    1: 39,
    2: 78,
    }
#max number of packs per row
maxnpacksperrow = 39
#ntotpacks
ntotpacks = 115
#id of first pack
firstpackid = startpacks[0]


def super_indexes( packid, tubeid, pixelid ):
    if packid < startpacks[1] : row = 0
    elif packid < startpacks[2] : row = 1
    else: row = 2
    stubeid = ( packid - startpacks[ row ] ) * ntubesperpack + tubeid
    spixelid = (1+row)*npixelspertube - 1 - pixelid
    return stubeid, spixelid


def packtube_from_supertubeid( super_tubeid, rowno = 0 ):
    return startpacks[rowno] + super_tubeid/ntubesperpack, super_tubeid % ntubesperpack


def pixel_from_superpixelid( super_pixelid ):
    return npixelspertube -1 - super_pixelid % npixelspertube


def detectorview( Ipdp_ ):
    '''create a histogram that is just a view of the original Ipdpt
    The horizontal axis is 'detectorID', which actually includes
    both the packID (in a detector array, top, middle, or bottom)
    and the detectorID relative to its parent pack.
    The vertial axis is 'pixelID', which actually is a combination
    of pixelID and the axis of (top, middle, bottom).
    '''
    horizontal = 'super-detectorID'
    vertical = 'super-pixelID'

    import histogram as H
    otheraxes = Ipdp_.axes()[3:]
    view = H.histogram(
        'view',
        [ (horizontal, range(0, maxnpacksperrow*ntubesperpack)),
          (vertical, range(0, npixelspertube*nrows)),
          ] + otheraxes )

    for packid in range(firstpackid, firstpackid+ntotpacks):
        for tubeid in range(0,ntubesperpack):
            stube, spixel = super_indexes( packid, tubeid, 0 )
            #print packid, tubeid
            slice = Ipdp_.I[ packid-firstpackid, tubeid ][ npixelspertube-1:None:-1 ]
            #print stube, spixel
            view.I[ stube, spixel-npixelspertube+1: spixel+1 ] = slice
            continue
        continue
    
    return view


def detectorview1( Ipdp_ ):
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
                       vertical: npixelspertube-1-pixel} ]=\
                      Ipdp_[ {'detectorpackID':pack,
                              'detectorID': tube,
                              'pixelID': pixel} ]

    return view


def test1():
    assert (super_indexes( 1, 1, 1 ) == 1,npixelspertube-2)
    assert (super_indexes( 39, 0, npixelspertube-1) == 0, npixelspertube )
    assert (super_indexes( 77, 0, 0) == 38*ntubesperpack, 2*npixelspertube-1)
    assert (super_indexes( 78, 5, npixelspertube-1) == 5, 2*npixelspertube)
    return


def test2():
    assert ( packtube_from_supertubeid( 1, rowno = 0 ) == (1,1) )
    assert ( pixel_from_superpixelid( npixelspertube - 2 ) == 1 )

    assert ( packtube_from_supertubeid( 0, rowno = 1 ) == (39,0) )
    assert ( pixel_from_superpixelid( npixelspertube ) == npixelspertube-1 )

    assert ( packtube_from_supertubeid( 38*ntubesperpack, rowno = 1 ) == (77,0) )
    assert ( pixel_from_superpixelid( 2*npixelspertube-1 ) == 0 )

    assert ( packtube_from_supertubeid( 5, rowno = 2 ) == (78,5) )
    assert ( pixel_from_superpixelid( 2*npixelspertube ) == npixelspertube-1 )
    return


def main():
    test1()
    test2()
    return


if __name__ == '__main__' : main()


# version
__id__ = "$Id$"

#  End of file 
