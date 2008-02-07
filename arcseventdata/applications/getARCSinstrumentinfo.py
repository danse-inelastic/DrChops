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


## This script create a bunch of pickled histograms containing
## ARCS instrument details such as
##   pixel-sample distances
##   pixel-position map
##
##   etc

import os

def run( ARCSxml ):
    from arcseventdata.getinstrumentinfo import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] ARCS.xml"
    parser = OptionParser(usage)

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    ARCSxml = args[0]
    run( ARCSxml )
    return

if __name__ == '__main__':
    import journal
    #journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
