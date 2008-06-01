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

        pathinh5 = pinv.str( 'pathinh5', default = '/' )
        pathinh5.meta['tip'] = 'path in the hdf5file where histogram will be saved'

        histogramname = pinv.str( 'histogramname', default = '' )
        histogramname.meta['tip'] = 'name of the histogram'

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
        self.compute()
        self.save()
        return


    def compute(self):
        import sys
        event_source = self.inventory.event_source

        nevents = int( self.inventory.nevents )
        if nevents == 0:
            ntotal = arcseventdata.getnumberofevents( event_source )
            nevents = ntotal
            pass
             
        reduction_args = self.build_args()
        
        engine = self.inventory.engine
        h = engine(event_source, nevents, *reduction_args )
        self.histogram = h

        self._info.log( "times: %s" % (os.times(),) )
        return


    def save(self):
        if self.mpiRank == 0:
            h5filename = self.h5filename
            self._info.log( "writing histogram to file %r" % h5filename )
            h = self.histogram
            histogramname = self.inventory.histogramname
            if histogramname != '':
                h.setAttribute( 'name', histogramname )
                
            from nx5.file import file
            if os.path.exists( h5filename ): mode ='w'
            else: mode = 'c'
            fs = file( h5filename, mode )._fs
            pathinh5 = self.pathinh5
            fs.makedirs( pathinh5 )
            
            from histogram.hdf import dump
            dump(h, h5filename, pathinh5, mode = 'w', fs = fs )
            pass
        return


    def _init(self):
        base._init(self)
        h5filename = self.inventory.h5filename
        pathinh5 = self.inventory.pathinh5
        #if os.path.exists(h5filename) and not overwrite:
        #    raise IOError, "%s already exists" % h5filename
        self.h5filename = h5filename
        self.pathinh5 = pathinh5
        return


    def _fini(self):
        base._fini(self)
        return
    
    pass # end of Application


import os
import arcseventdata
    

# version
__id__ = "$Id$"

# End of file 
