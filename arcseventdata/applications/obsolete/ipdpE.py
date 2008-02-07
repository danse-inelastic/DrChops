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
## and create a histogram hdf5 file of I(pack, detector, pixel, E)


import os

def run( eventdatafilename, nevents, ARCSxml, h5filename,
         E_params, Ei, emission_time = 0 ):

    from arcseventdata.getinstrumentinfo import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    npacks, ndetsperpack, npixelsperdet = infos['detector-system-dimensions']
    mod2sample = infos['moderator-sample distance']
    pixelPositionsFilename = infos['pixelID-position mapping binary file']
    
    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "pixel-positions-filename=%s" % pixelPositionsFilename
    print "output h5filename = %s" % h5filename
    print 'E_params (unit: angstrom) = %s' % (E_params, )
    print 'mod2sample distance = %s' % mod2sample
    print 'Incident energy (unit: meV) = %s' % (Ei, )
    print 'emission_time (unit: microsecond) = %s' % (emission_time, )

    if os.path.exists(h5filename):
        raise IOError, "%s already exists" % h5filename

    E_begin, E_end, E_step = E_params # angstrom

    import arcseventdata, histogram 
    E_axis = histogram.axis('energy', boundaries = histogram.arange(
        E_begin, E_end, E_step) )
    h = histogram.histogram(
        'I(pdpE)',
        [
        ('detectorpackID', range(npacks+1)),
        ('detectorID', range(ndetsperpack)),
        ('pixelID', range(npixelsperdet) ),
        E_axis,
        ],
        data_type = 'int',
        )

    events = arcseventdata.readevents( eventdatafilename, nevents )
    pixelPositions = arcseventdata.readpixelpositions( pixelPositionsFilename )
    
    arcseventdata.events2IpdpE(
        events, nevents, h, Ei, pixelPositions,
        npacks = npacks, ndetsperpack = ndetsperpack, npixelsperdet = npixelsperdet,
        mod2sample = mod2sample,
        emission_time = emission_time,
        )
    
    # set error bar squares to be equal to counts
    h.errors().storage().asNumarray()[:] = h.data().storage().asNumarray()
    
    from histogram.hdf import dump
    dump(h, h5filename, '/', 'c' )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)
    #parser.add_option("-e", "--eventdatafile", dest="eventdatafile",
    #                  help="ARCS event data file")
    parser.add_option("-o", "--out", dest="h5filename", default = "Idspacing.h5",
                      help="hdf5 file of I(dspacing) histogram")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-E", "--EnergyTransfer", dest="E_params", default = '-50,50,1.',
                      help="energy transfer bin parameters (begin, end, step). units: meV")
    parser.add_option("-x", "--ARCS-xml", dest = "ARCSxml",
                      default = "ARCS.xml",
                      help="ARCS instrument xml file" )
    parser.add_option('-I', '--IncidentEnergy', dest='Ei', default = 60, type = 'float',
                      help='incident energy. unit: meV')
    parser.add_option('-t', '--emission_time', dest='emission_time', default = 0.0, type = 'float',
                      help='emission time. tof reading - real tof. unit: microsecond')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    h5filename = options.h5filename
    nevents = options.nevents
    E_params = eval( options.E_params )
    Ei = options.Ei
    emission_time = options.emission_time
    ARCSxml = options.ARCSxml

    run( eventdatafile, nevents, ARCSxml, h5filename, E_params, Ei, emission_time )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
