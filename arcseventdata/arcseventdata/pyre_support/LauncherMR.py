#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# special launcher for upgrayedd.danse.us


from mpi.Launcher import Launcher


class LauncherMR(Launcher):


    class Inventory(Launcher.Inventory):

        import pyre.inventory

        dry = pyre.inventory.bool("dry", default=False)
        debug = pyre.inventory.bool("debug", default=False)
        command = pyre.inventory.str("command", default="mr")
        extra = pyre.inventory.str("extra", default="")
        nodes = pyre.inventory.str("nodes", default="")
        python_mpi = pyre.inventory.str("python-mpi", default="`which mpipython.exe`")


    def launch(self):
        args = self._buildArgumentList()
        if not args:
            return False
        
        command = " ".join(args)
        self._info.log("executing: {%s}" % command)

        dry = self.inventory.dry
        if not dry:
            import os
            os.system(command)
            return True

        return False

            
    def __init__(self):
        Launcher.__init__(self, "mr")
        return


    def _buildArgumentList(self):
        nodes = self.inventory.nodes
        if not nodes: return []
        
        import os
        nodes = os.path.expanduser(nodes)
        if not os.path.exists(nodes): 
            raise RuntimeError, "No such file %s" % nodes
        if nodes != 'mr.nodes':
            import shutil
            shutil.copyfile(nodes, 'mr.nodes')

        import sys

        python_mpi = self.inventory.python_mpi

        # build the command
        args = []
        args.append(self.inventory.command)
        args.append(self.inventory.extra)

        # add the parallel version of the interpreter on the command line
        args.append(python_mpi)

        sysargs = sys.argv
        args.append( sysargs[0] )
        args.append("--mode=worker")
        args += sysargs[1:]

        return args


# version
__id__ = "$Id: LauncherMR.py,v 1.1.1.1 2005/03/08 16:13:30 aivazis Exp $"

# End of file 
