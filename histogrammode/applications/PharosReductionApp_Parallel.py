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


'''
rsh n01 mpdboot -n 1 -f mpd.hosts
rsh -. n01 "PharosReductionApp.py  -launcher.nodelist=1 -launcher.nodegen='n%02d:2' -launcher.nodes=2 -journal.info.mpi -journal.info.mpirun "
rsh n01 mpdallexit

'''



from PowderReductionApp_Parallel import PowderReductionApp as base

class PharosReductionApp( base ):

    class Inventory(base.Inventory):
        pass

    def __init__(self, name = "PharosReductionApp" ):
        base.__init__(self, name )
        return

    pass # end of PharosReductionApp

def main():
    app = PharosReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
