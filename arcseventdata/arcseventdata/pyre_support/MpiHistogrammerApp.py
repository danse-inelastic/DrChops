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
        sys.argv = [sys.argv[0]] + _mergeArgs(sys.argv[1:])
        source = sys.argv[-1]
        if not source.startswith( '-' ):
            sys.argv[-1] = '--event-source=%s' % source
            pass
        print sys.argv
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
        nevents = int(self.inventory.nevents)

        event_source = self.inventory.event_source
        eventfiles = event_source.split(',')
        if len(eventfiles)>1 and nevents!=0:
            raise RuntimeError, "You have selected to reduce multiple event files, which makes your selection of number-of-events not meaningful."

        if len(eventfiles)==0:
            raise RuntimeError, 'You have not specify any event files'

        if len(eventfiles)==1:
            h = self.process_one_file(event_source, nevents)
        else:
            hists = [self.process_one_file(f) for f in eventfiles]
            assert len(hists)>1
            h = hists[0]
            if self.mpiRank==0:
                for h1 in hists[1:]: h += h1

        self.histogram = h
        self._info.log( "times: %s" % (os.times(),) )
        return

    
    def process_one_file(self, path, nevents=0):
        if nevents == 0:
            ntotal = arcseventdata.getnumberofevents( path )
            nevents = ntotal
            pass
        
        reduction_args = self.build_args()
        
        engine = self.inventory.engine
        return engine(path, nevents, *reduction_args )


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


def _mergeArgs(argv):
    index = len(argv)
    iargv = list(argv); iargv.reverse()
    for i, arg in enumerate(iargv):
        if arg.startswith('-'): index = i; break
        continue

    # index will be the index of the first arg (not options)
    index = len(argv)-index
    
    lastopt = argv[index-1]
    if lastopt.startswith('-') and '=' not in lastopt and not lastopt.startswith('--'):
        index += 1
    if index >= len(argv): return argv
    opts = argv[:index]
    args = argv[index:]
    return opts + [','.join(args)]


import os
import arcseventdata
    

# version
__id__ = "$Id$"

# End of file 
