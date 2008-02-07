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


## This script print out number of events of a pre-nexus file


import os

def run( eventdatafilename ):
    from arcseventdata import getnumberofevents
    print getnumberofevents( eventdatafilename )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)

    #parser.add_option("-o", "--out", dest="h5filename", default = "Itof.h5",
    #                  help="hdf5 file of I(tof) histogram")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]

    run( eventdatafile)
    return

if __name__ == '__main__':
    main()
    

# version
__id__ = "$Id$"

# End of file 
