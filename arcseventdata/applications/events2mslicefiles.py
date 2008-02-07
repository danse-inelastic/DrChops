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


## This script read events from ARCS event-mode preNexus file
## and write mslice spe and phx files


import os

def run( eventdatafilename, nevents, ARCSxml,
         mslicefileprefix,
         E_params, Ei,
         ):
    
    from arcseventdata.getinstrumentinfo import getinstrumentinfo
    infos = getinstrumentinfo(ARCSxml)
    npacks, ndetsperpack, npixelsperdet = infos['detector-system-dimensions']
    mod2sample = infos['moderator-sample distance']
    pixelPositionsFilename = infos['pixelID-position mapping binary file']

    print "eventdatafilename = %s" % eventdatafilename
    print "nevents = %s" % nevents
    print "pixel-positions-filename=%s" % pixelPositionsFilename
    print "output mslicefileprefix = %s" % mslicefileprefix
    print 'E_params (unit: meV) = %s' % (E_params, )

    spef = '%s.spe' % mslicefileprefix
    phxf = '%s.phx' % mslicefileprefix
    
    if os.path.exists(spef) or os.path.exists(phxf):
        raise IOError, "%s or %s already exists" % (spef, phxf)

    #first integrate events to I(pack,det,pix,E)
    E_begin, E_end, E_step = E_params # meV

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
    
    events, nevents = arcseventdata.readevents( eventdatafilename, nevents )
    pixelPositions = arcseventdata.readpixelpositions(
        pixelPositionsFilename )
    
    arcseventdata.events2IpdpE(
        events, nevents, h, Ei, pixelPositions,
        npacks = npacks, ndetsperpack = ndetsperpack,
        npixelsperdet = npixelsperdet,
        mod2sample = mod2sample,
        )

    #get phi(pixel), psi(pixel)
    s = open( pixelPositionsFilename ).read()
    from numpy import fromstring
    positions = fromstring( s, 'd' )

    phi_p, psi_p = arcseventdata.pixelpositions2angles(
        positions, npacks, ndetsperpack, npixelsperdet)

    #convert to mslice file
    arcseventdata.write_mslice_files(
        h[{'detectorpackID':(1,None)}],
        phi_p[{'detectorpackID':(1,None)}],
        psi_p[{'detectorpackID':(1,None)}],
        spef, phxf )
    return


def main():
    from optparse import OptionParser
    usage = "usage: %prog [options] event-data-file"
    parser = OptionParser(usage)

    parser.add_option("-o", "--out", dest="mslicefileprefix", default = "run5",
                      help="prefix of mslice data files to be writen")
    parser.add_option("-n", "--nevents", dest="nevents", default = '1000',
                      type = 'int', help="number of events")
    parser.add_option("-E", "--EnergyTransfer", dest="E_params", default = '-50,50,1.',
                      help="energy transfer bin parameters (begin, end, step). units: meV")
    parser.add_option("-x", "--ARCSxml", dest = "ARCSxml",
                      default = "ARCS.xml",
                      help="ARCS instrument xml" )
    parser.add_option('-I', '--IncidentEnergy', dest='Ei', default = 60, type = 'float',
                      help='incident energy. unit: meV')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        raise "should not reach here"

    eventdatafile = args[0]
    mslicefileprefix = options.mslicefileprefix
    nevents = options.nevents
    E_params = eval( options.E_params )
    Ei = options.Ei
    ARCSxml = options.ARCSxml

    run( eventdatafile, nevents, ARCSxml,
         mslicefileprefix, E_params, Ei )
    return

if __name__ == '__main__':
    import journal
    journal.warning( 'arcseventdata.Histogrammer2' ).deactivate()
    main()
    

# version
__id__ = "$Id$"

# End of file 
