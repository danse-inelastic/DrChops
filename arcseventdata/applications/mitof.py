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


## This script read monitor data file and create a I(tof) histogram


import os

def run( monitordatafilename, h5filename,
         tof_params = None,
         nevents = None,
         ):

    print "monitordatafilename = %s" % monitordatafilename
    print "nevents = %s" % nevents
    print "output h5filename = %s" % h5filename
    print 'tof_params (unit: us) = %s' % (tof_params, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    from arcseventdata.monitorData import readHistogram
    h = readHistogram( monitordatafilename )
    
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )

    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)

    parser.add_option(
        "-o", "--out", dest="h5filename", default = "monitor1-Itof.h5",
        help="hdf5 file of a monitor I(tof) histogram")
##     parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
##                       type = 'int', help="number of events")
##     parser.add_option("-t", "--tpf", dest="tof_params", default = '0,100,0.1',
##                       help="tof bin parameters (begin, end, step). units: us")
##     parser.add_option("-x", "--ARCSxml", dest = "ARCSxml",
##                       default = "ARCS.xml",
##                       help="ARCS instrument xml" )

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

##     ARCSxml = options.ARCSxml
    monitordatafilename = args[0]
    h5filename = options.h5filename
##     nevents = options.nevents
##     tof_params = eval( options.tof_params )

    #run( eventdatafile, nevents, h5filename, tof_params, ARCSxml)
    run( monitordatafilename, h5filename )
    return

if __name__ == '__main__':
    import journal
    #journal.warning( 'arcseventdata.Histogrammer1' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
