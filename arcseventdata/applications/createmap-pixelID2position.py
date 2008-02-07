#!/usr/bin/env python

# This script creates the map to convert pixelID to the postion of the pixel


from arcseventdata.createmap_pixelID2position import createmap


def help():
    msg = '''
createmap-pixelID2position.py  ARCS.xml
'''
    print msg
    return


def main():
    import sys
    if len(sys.argv) != 2:
        help()
        exit(1)
    arcsxml = sys.argv[1]

    from instrument.nixml import parse_file
    arcs = parse_file( arcsxml )

    nPixelsPerDetector = 128
    nDetectorsPerPack = 8
    nPacks = len(arcs.getDetectorSystem().elements())
    
    pixelID2position = createmap( arcs, nPixelsPerDetector, nDetectorsPerPack, nPacks )

    import pickle
    pickle.dump( pixelID2position, open('pixelID2position.pkl','w'))

    open('pixelID2position.bin','w').write( pixelID2position.tostring() )
    return


if __name__ == '__main__': main()

    
