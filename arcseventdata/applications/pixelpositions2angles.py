#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## This script converts pixelpositions binary file
## to histograms psi(pixel) and phi(pixel)


import os

def run( pixelPositionsFilename, h5filename,
         npacks = 115, ndetsperpack = 8, npixelsperdet = 128):
    
    print "pixel-positions-filename=%s" % pixelPositionsFilename
    print "output h5filename = %s" % h5filename

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    s = open( pixelPositionsFilename ).read()
    from numpy import fromstring
    positions = fromstring( s, 'd' )

    import arcseventdata
    phi_p, psi_p = arcseventdata.pixelpositions2angles(
        positions, npacks, ndetsperpack, npixelsperdet)

    from histogram.hdf import dump
    dump(phi_p, h5filename, '/', 'c' )
    dump(psi_p, h5filename, '/', 'w' )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] pixel-positions-file"
    parser = OptionParser(usage)

    parser.add_option("-o", "--out", dest="h5filename", default = "angles.h5",
                      help="hdf5 file of phi(pixel) and psi(pixel) histograms")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    h5filename = options.h5filename
    pixelPositionsFilename = args[0]

    run( pixelPositionsFilename, h5filename )
    return


if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
