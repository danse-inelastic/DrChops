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
This module is intended to create a 2D view of intensities
that roughly looks like what you can see from the sample position
to the detector.

The original histograms collected have 3 indexes for indexing a
pixel (packid, tubeid, pixelid). 

Here we define super indexes so that we can have 2D detector view
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
# short packs
shortpack1 = 70
shortpack2 = 71
shortpacks = [shortpack1, shortpack2]
slratios = {
    shortpack1: 0.38,
    shortpack2: 0.28,
    }
#max number of packs per row
# 38 packs per row for upper and lower rows.
# 39 packs in the middle row. But because we combine the
# shorter packs to one pack, so we can reduce 39 by 1.
maxnpacksperrow = max(38, 39-1, 38)
#ntotpacks
ntotpacks = 115
#id of first pack
firstpackid = startpacks[0]


def super_indexes( packid, tubeid, pixelid ):
    '''convert pack id, tube id, pixel id to super tube id and super pixel id
    '''
    if packid in shortpacks:
        handler = eval('super_indexes_%s' % packid)
        return handler(tubeid, pixelid)
    if packid < startpacks[1] : row = 0
    elif packid < startpacks[2] : row = 1
    else: row = 2
    stubeid = ( packid - startpacks[ row ] ) * ntubesperpack + tubeid
    
    # need to move the two short packs to one super pack
    # and the packs after short pack #2 of row 1 should be moved
    # to the left
    if row == 1 and packid > shortpack2: stubeid -= ntubesperpack
    
    spixelid = (1+row)*npixelspertube - 1 - pixelid
    return stubeid, spixelid


def super_indexes_70(tubeid, pixelid):
    stubeid = (shortpack1-startpacks[1]) * ntubesperpack + tubeid
    ratio = slratios[70]
    spixelid = int((ratio+1)*npixelspertube - 1 - pixelid*ratio)
    return stubeid, spixelid


def super_indexes_71(tubeid, pixelid):
    ratio = slratios[71]
    stubeid = (shortpack1-startpacks[1]) * ntubesperpack + tubeid
    spixelid = int((1+1)*npixelspertube - 1 - pixelid*ratio)
    #print tubeid, pixelid, stubeid, spixelid
    return stubeid, spixelid


supertubeid_shorttubestart = ntubesperpack * (shortpack1-startpacks[1])
supertubeid_shorttubeend = supertubeid_shorttubestart + ntubesperpack
def packtube_from_supertubeid( super_tubeid, rowno = 0, super_pixelid=None ):
    '''convert super tube id to pack id and tube id

    super_tubeid: the super tube id
    rowno: the row number (down to up: 0,1,2)
    super_pixelid: the super pixel id. This is needed for pixels in the short packs
    '''
    if rowno == 1:
        if super_tubeid >= supertubeid_shorttubestart \
               and super_tubeid < supertubeid_shorttubeend:
            return packtube_from_supertubeid_inshortpacks(super_tubeid, super_pixelid)
        elif super_tubeid >= supertubeid_shorttubeend:
            return packtube_from_supertubeid_aftershortpacks(super_tubeid)
    
    return startpacks[rowno] + super_tubeid/ntubesperpack, super_tubeid % ntubesperpack

def packtube_from_supertubeid_inshortpacks(super_tubeid, super_pixelid):
    if super_pixelid < 1.5*npixelspertube:
        # pack 70
        return shortpack1, super_tubeid%ntubesperpack
    else:
        # pack 71
        return shortpack2, super_tubeid%ntubesperpack

def packtube_from_supertubeid_aftershortpacks(super_tubeid):
    rowno = 1
    return startpacks[rowno] + super_tubeid/ntubesperpack + 1, super_tubeid % ntubesperpack

def pixel_from_superpixelid( super_pixelid, super_tubeid=None ):
    '''convert super pixel id to pixel id

    super_pixelid: the super pixel id
    super_tubeid: the super tube id. This is needed for pixels in the short packs
    '''
    if super_tubeid >= supertubeid_shorttubestart \
       and super_tubeid < supertubeid_shorttubeend :
        return pixel_from_superpixelid_inshortpacks(super_pixelid)
    return npixelspertube -1 - super_pixelid % npixelspertube


def pixel_from_superpixelid_inshortpacks(super_pixelid):
    if super_pixelid < 1.5*npixelspertube:
        pack = 70
        ratio = slratios[pack]
        start = int(npixelspertube-1-(super_pixelid-npixelspertube)/ratio)
        step = int(1./ratio +0.5)
        return start-step, start
    else:
        pack = 71
        ratio = slratios[pack]
        start = int((2*npixelspertube-1-super_pixelid)/ratio)
        step = int(1./ratio+0.5)
        return start, start+step


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

            if packid not in shortpacks:
                #print packid, tubeid
                slice = Ipdp_.I[ packid-firstpackid, tubeid ][ npixelspertube-1:None:-1 ]
                #print stube, spixel
                view.I[ stube, spixel-npixelspertube+1: spixel+1 ] = slice
            else:
                for pixelid in range(0, npixelspertube):
                    stube, spixel = super_indexes(packid, tubeid, pixelid)
                    slice = Ipdp_.I[packid-firstpackid, tubeid, pixelid]
                    view.I[stube, spixel] += slice
                    #print packid, npixelspertube, pixelid, spixel
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
    assert (super_indexes( 77, 0, 0) == 37*ntubesperpack, 2*npixelspertube-1)
    assert (super_indexes( 78, 5, npixelspertube-1) == 5, 2*npixelspertube)
    return


def test2():
    assert ( packtube_from_supertubeid( 1, rowno = 0 ) == (1,1) )
    assert ( pixel_from_superpixelid( npixelspertube - 2 ) == 1 )

    assert ( packtube_from_supertubeid( 0, rowno = 1 ) == (39,0) )
    assert ( pixel_from_superpixelid( npixelspertube ) == npixelspertube-1 )

    assert ( packtube_from_supertubeid( 37*ntubesperpack, rowno = 1 ) == (77,0) )
    assert ( pixel_from_superpixelid( 2*npixelspertube-1 ) == 0 )

    assert ( packtube_from_supertubeid( 5, rowno = 2 ) == (78,5) )
    assert ( pixel_from_superpixelid( 2*npixelspertube ) == npixelspertube-1 )
    assert ( packtube_from_supertubeid( 248, rowno=1, super_pixelid=209) == (71,0) )
    assert ( packtube_from_supertubeid( 251, rowno=1, super_pixelid=212) == (71,3) )
    assert ( packtube_from_supertubeid( 248, rowno=1, super_pixelid=170) == (70,0) )
    assert ( packtube_from_supertubeid( 251, rowno=1, super_pixelid=170) == (70,3) )

    assert pixel_from_superpixelid(128+127, super_tubeid=248)==(0,3)
    assert pixel_from_superpixelid(128, super_tubeid=248)==(123,127)
    return


def main():
    test1()
    test2()
    return


if __name__ == '__main__' : main()


# version
__id__ = "$Id$"

#  End of file 
