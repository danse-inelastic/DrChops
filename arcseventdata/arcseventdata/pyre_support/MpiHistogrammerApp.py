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


## base class of mpi histogrammer application. derived from MpiApplication.
## The customization done here are:


from MpiApplication import Application as base

class Application(base):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        h5filename = pinv.str( 'o', default = "" )
        h5filename.meta['tip'] ="hdf5 file for output histogram"

        nevents = pinv.float( "n", default = 0 )
        nevents.meta['tip'] ="number of events to reduce"

        engine = pinv.facility( 'engine', default = None )
        engine.meta['tip'] = 'histogrammer engine'

        event_source = pinv.str( 'event-source', default = '' )

        pass # end of Inventory


    def __init__(self, name):
        #event stream source arguments will be the last argument
        import sys
        source = sys.argv[-1]
        if not source.startswith( '-' ):
            sys.argv[-1] = '--event-source=%s' % source
            pass
        base.__init__(self, name)
        return


    def help(self):
        import sys, os
        print "%s [options] event-file-name" % os.path.split( sys.argv[0] )[-1]
        print
        print "Options: "
        base.help(self)
        return


    def build_args(self): raise NotImplementedError


    def main(self):
        import sys
        event_source = self.inventory.event_source

        nevents = int( self.inventory.nevents )
        if nevents == 0:
            ntotal = arcseventdata.getnumberofevents( event_source )
            nevents = ntotal
            pass
             
        h5filename = self.inventory.h5filename
        
        if os.path.exists(h5filename):
            raise IOError, "%s already exists" % h5filename

        reduction_args = self.build_args()
        
        engine = self.inventory.engine
        h = engine(event_source, nevents, *reduction_args )

        if self.mpiRank == 0:
            self._info.log( "writing histogram to file %r" % h5filename )
            from histogram.hdf import dump
            dump(h, h5filename, '/', 'c' )
            pass
        return    
    
    pass # end of Application


import os
import arcseventdata
    

# version
__id__ = "$Id$"

# End of file 
