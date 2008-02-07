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


## This script reads events from event data file
## and create a histogram hdf5 file of I(pix)


# This script use the c++ program "ipix" to extract I(pix) from
# an event-mode data file of ARCS, and save the histogram to a 2col ascii file.
# Then the ascii file is read, and a histogram object is created, and
# the histogram object is saved in a h5 file so that it is easier
# to manipulate in HistogramGUI.

import os

def run( eventdatafilename, nevents, h5filename, pixparams ):
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "output h5filename = %s" % h5filename
    print 'pixelID params = %s' % (pixparams, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    pixbegin, pixend, pixstep = pixparams 
    
    ipixdat = 'Ipix.%s-%s-%s.dat' % (
        eventdatafilename, nevents, pixparams)
    cmd = 'ipix "%s" %s %s %s %s "%s" ' % (
        eventdatafilename, nevents,
        pixbegin, pixend, pixstep, 
        ipixdat )
    if os.system( cmd ): raise "%s failed" % cmd

    if not os.path.exists( ipixdat ): raise "%s was not created" % ipixdat

    from arcseventdata.histogramFrom2colascii import convert
    h = convert( ipixdat, name = "I(pix)", xname = 'pixelID', xunit = '1' )
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)
    #parser.add_option("-e", "--eventdatafile", dest="eventdatafile",
    #                  help="ARCS event data file")
    parser.add_option("-o", "--out", dest="h5filename", default = "IpixelID.h5",
                      help="hdf5 file of I(pixelID) histogram")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-p", "--pixelID", dest="pixparams", default = '0,102400,1024',
                      help="pix bin parameters (begin, end, step)")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    h5filename = options.h5filename
    nevents = options.nevents
    pixparams = eval( options.pixparams )

    run( eventdatafile, nevents, h5filename, pixparams )
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
