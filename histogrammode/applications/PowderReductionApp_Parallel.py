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




from mpi.Application import Application as base



class PowderReductionApp(base):


    class Inventory( base.Inventory ):
        
        import pyre.inventory as inv

        from reduction.pyre.PowderReduction import PowderReduction as PRComp
        reducer = inv.facility('reducer', factory= PRComp)

        pass #

    Inventory.mode.meta['opacity'] = 10
    Inventory.launcher.meta['opacity'] = 10


    def __init__(self, name='PowderReductionApp'):
        base.__init__(self, name)
        return


    def main(self):
        self.inventory.reducer.getOutput( 'sqe' )
        return


    pass # end of PowderReductionApp


def main():
    app = PowderReductionApp()
    app.run()
    import os
    print "times: %s" % str(os.times())
    return


if __name__ == '__main__': main()
