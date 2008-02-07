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


## base class of mpi application. derived from pyre mpi application.
## The customization done here are:
##  1. use mpich2 launcher
##  2. support -o output and -o=output
##  3. inherit also from ParallelComponent so we have access to self.mpiRank and other mpi thing.
##  4. build a help message out of meta['tip']


from mpi.Application import Application as base
from arcseventdata.ParallelComponent import ParallelComponent


class Application(base, ParallelComponent):

    class Inventory(base.Inventory):

        import pyre.inventory as pinv

        pass # end of Inventory


    def __init__(self, name):
        base.__init__(self, name)
        self._normalizeSysArgv()
        return


    def help(self):
        excluded = [
            'typos',
            'help-persistence',
            'help',
            'launcher',
            'journal',
            'help-properties',
            'mode',
            'weaver',
            'help-components',
            
            'engine',
            'event-source',
            ]
        for name in self.inventory.propertyNames():
            if name in excluded: continue
            trait = self.inventory.getTrait( name )
            print '  -%s: %s, default = %s' % (
                name, trait.meta.get('tip') or '', trait.default )
        return


    def _defaults(self):
        from LauncherMPICH2 import LauncherMPICH2
        self.inventory.launcher = LauncherMPICH2()
        return


    def _normalizeSysArgv(self):
        #convert -o output.filename to -o=output.filename
        import sys
        argv = sys.argv
        new = [ argv [0], ]
        for arg in argv[1:]:
            if arg.startswith( '--' ):
                new.append( arg )
            elif arg.startswith( '-' ) and '=' in arg:
                new.append( arg )
            elif arg.startswith( '-' ) and len(arg)==2:
                new.append( arg )
            else:
                new[-1] += '=%s' % arg
                pass
            continue
        sys.argv = new
        
        self._debug.log( 'sys.argv=%s' % (sys.argv, ) )
        return

    pass # end of Application

    

# version
__id__ = "$Id$"

# End of file 
