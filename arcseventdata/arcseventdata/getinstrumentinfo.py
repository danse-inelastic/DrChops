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


## obtain instrument information such as
##   * mod2sample distance
##   * number of packs, # of dets per pack, # of pixels per detector
##   * pixelID2positions mapping file
##   * etc etc
##
## we need a caching mechanism so that we don't need to redo
## this every time.


cache_name = 'ARCSinfo-cache'
def cache_path( ARCSxml ):
    xmlrealpath = os.path.realpath( ARCSxml )
    dirofxml = os.path.dirname( xmlrealpath )
    candidate = os.path.join( dirofxml, cache_name )
    if os.path.exists(candidate) and os.path.isdir( candidate ):
        return candidate
    return cache_name


def isWritable( path ):
    import tempfile
    try:
        t = tempfile.mkdtemp( dir = path )
    except:
        return False
    os.rmdir( t )
    return True


def getinstrumentinfo( ARCSxml ):
    if _new(ARCSxml): _updateCache( ARCSxml )
    return _getInfoFromCache( ARCSxml )


def _new(ARCSxml):
    from os.path import getmtime, exists, isfile
    xmlmtime = getmtime( ARCSxml )
    cache_dir = cache_path( ARCSxml )
    
    for file in files:
        file = os.path.join( cache_dir, file )
        if not exists(file): return True
        if not isfile(file): return True
        if getmtime( file ) < xmlmtime: return True
        continue
    return False


def _updateCache(ARCSxml):
    ARCSxml = os.path.abspath( ARCSxml )
    cache_dir = os.path.abspath( cache_path( ARCSxml ) )
    if not os.path.exists( cache_dir ):
        os.makedirs( cache_dir )
    assert isWritable( cache_dir ), "Cache path %s is not writable" % (
        cache_dir, )
    cwd = os.path.abspath( os.curdir )
    os.chdir( cache_dir )
    
    print "parsing ARCS instrument xml"
    from instrument.nixml import parse_file
    instrument = parse_file( ARCSxml )
    geometer = instrument.geometer

    print "generating ARCS instrument info dictionary"
    from reduction.core.getPixelInfo import getDetectorAxes
    detaxes = getDetectorAxes( instrument )

    packAxis, tubeAxis, pixelAxis = detaxes

    nPacks = packAxis.size()
    nDetectorsPerPack = tubeAxis.size()
    nPixelsPerDetector = pixelAxis.size()

    from createmap_pixelID2position import createmap
    pixelID2position = createmap( instrument, nPixelsPerDetector, nDetectorsPerPack, nPacks )

    print "saving ARCS instrumentn info to files"
    pickle.dump( pixelID2position, open('pixelID2position.pkl','w'))

    open('pixelID2position.bin','w').write( pixelID2position.tostring() )

    mod2sample = geometer.distanceToSample( instrument.getModerator() )
    mod2mon1 = geometer.distance( instrument.getModerator(),
                                  instrument.getMonitors()[0] )
    mod2mon2 = geometer.distance( instrument.getModerator(),
                                  instrument.getMonitors()[1] )

    infos = {
        'detector-system-dimensions' :
        [nPacks, nDetectorsPerPack, nPixelsPerDetector],
        'moderator-sample distance': mod2sample,
        'moderator-monitor1 distance': mod2mon1,
        'moderator-monitor2 distance': mod2mon2,
        }

    pickle.dump( infos, open('ARCS-instrument-info.pkl', 'w') )

    from getpixelinfo import getpixelinfo
    phi_p, psi_p, dist_p = getpixelinfo(
        pixelID2position, 
        npacks = nPacks, ndetsperpack = nDetectorsPerPack,
        npixelsperdet = nPixelsPerDetector )

    pickle.dump( phi_p, open('phi_pdp.pkl', 'w') )
    pickle.dump( psi_p, open('psi_pdp.pkl', 'w') )
    pickle.dump( dist_p, open('dist_pdp.pkl', 'w') )

    os.chdir( cwd )
    return


def _getInfoFromCache( ARCSxml ):
    cwd = os.path.abspath( os.curdir )
    cache_dir = cache_path( ARCSxml )
    os.chdir( cache_dir )
    infos = pickle.load( open('ARCS-instrument-info.pkl' ) )
    os.chdir( cwd )
    infos[ 'pixelID-position mapping binary file' ] =  os.path.join(
        cache_dir, 'pixelID2position.bin' )
    import units
    meter = units.length.meter
    for k,v in infos.iteritems():
        if k.endswith('distance'): infos[k] = infos[k] / meter
        pass
    return infos

files = [
    'pixelID2position.pkl',
    'pixelID2position.bin',
    'ARCS-instrument-info.pkl',
    'phi_pdp.pkl',
    'psi_pdp.pkl',
    'dist_pdp.pkl',
    ]


import pickle
import os

# version
__id__ = "$Id$"

#  End of file 
