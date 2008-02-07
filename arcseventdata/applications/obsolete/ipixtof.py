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
## and create a histogram hdf5 file of I(pix, tof)


# This script use the c++ program "ipixtof" to extract I(pix,tof) from
# an event-mode data file of ARCS, and save the histogram to a raw binary file.
# Then the binary file is read into python,
# and a histogram object is created, and
# the histogram object is saved in a h5 file so that it is easier
# to manipulate in HistogramGUI later.

import os

def run( eventdatafilename, nevents, h5filename, pixparams, tofparams,
         nPixelsPerDetector=128, nDetectorsPerPack=8 ):
    nPixelsPerPack = nPixelsPerDetector * nDetectorsPerPack
    
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "output h5filename = %s" % h5filename
    print 'tofparams (microseconds) = %s' % (tofparams, )
    print 'pixelID params = %s' % (pixparams, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    #make sure tofparams are integers multiply 100ns
    for t in tofparams: assert t*10 - int(t*10) <= 1e-6*t
    tofbegin, tofend, tofstep = tofparams # microsecond

    #pix parameters
    pixbegin, pixend, pixstep = pixparams
    #check pixstep
    assert pixstep < nPixelsPerDetector and nPixelsPerDetector % pixstep == 0 or \
           pixstep % nPixelsPerDetector == 0 , \
           'pixstep must be either a division of nPixelsPerDetector '\
           'or a multiple of nPixelsPerDetector: '\
           'pixstep = %s, nPixelsPerDetector = %s' % (
        pixstep, nPixelsPerDetector )
    assert pixstep < nPixelsPerPack and nPixelsPerPack % pixstep == 0 or \
           pixstep % nPixelsPerPack == 0 , \
           'pixstep must be either a division of nPixelsPerPack '\
           'or a multiple of nPixelsPerPack: '\
           'pixstep = %s, nPixelsPerPack = %s' % (
        pixstep, nPixelsPerPack )
    
    iptdat = 'Ipixtof.%s-%s-%s-%s(microseconds).dat' % (
        eventdatafilename, nevents, pixparams, tofparams)
    cmd = 'ipixtof "%s" %s %s %s %s %s %s %s "%s" ' % (
        eventdatafilename, nevents,
        pixbegin, pixend, pixstep,
        tofbegin*10, tofend*10, tofstep*10, # 100 ns
        iptdat )
    if os.system( cmd ): raise "%s failed" % cmd

    if not os.path.exists( iptdat ): raise "%s was not created" % iptdat

    from histogram import histogram, axis
    pixaxis = axis('pixelID', range( 0, nPixelsPerDetector, pixstep ) )
    detaxis = axis('detectorID',
                   range( 0, nDetectorsPerPack,
                          pixstep<nPixelsPerDetector or pixstep/nPixelsPerDetector ) )
    dpaxis = axis('detectorpackID', range(
        pixbegin/nPixelsPerPack, pixend/nPixelsPerPack,
        pixstep < nPixelsPerPack or pixstep/nPixelsPerPack )
                  )
    import numpy as N
    tofaxis = axis('tof', boundaries=N.arange( tofbegin, tofend+tofstep, tofstep ),
                   unit = 'microsecond' )
    stor = readArray( iptdat, 'u4',
                      (dpaxis.size(), detaxis.size(), pixaxis.size(), tofaxis.size()))
    
    h = histogram( "Ipdpt",
                   [ dpaxis, detaxis, pixaxis, tofaxis ],
                   data = stor )
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )
    return


def readArray( filename, type, shape ):
    #read a binary data file and convert to a data array
    #read as astring
    s = open(filename).read()
    #convert to array
    return bytes2array( s, type, shape )


def bytes2array( s, type, shape ):
    #convert a string to a numpy array
    import numpy
    a = numpy.fromstring( s, type )
    try:
        a.shape = shape
    except:
        raise ValueError, "shape mismatch: %s, %s" % (shape, a.shape) 
    return a


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)
    #parser.add_option("-e", "--eventdatafile", dest="eventdatafile",
    #                  help="ARCS event data file")
    parser.add_option("-o", "--out", dest="h5filename", default = "Ipdpt.h5",
                      help="hdf5 file of I(pix,tof) histogram")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-t", "--tof", dest="tofparams", default = '0,10000, 100',
                      help="tof bin parameters (begin, end, step). units: microsecond")
    parser.add_option("-p", "--pixelID", dest="pixparams", default = '0,102400,1024',
                      help="pix bin parameters (begin, end, step)")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    h5filename = options.h5filename
    nevents = options.nevents
    tofparams = eval( options.tofparams )
    pixparams = eval( options.pixparams )

    run( eventdatafile, nevents, h5filename, pixparams, tofparams )
    return

if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
