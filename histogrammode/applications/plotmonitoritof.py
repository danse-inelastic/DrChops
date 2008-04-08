#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from pyre.applications.Script import Script


class PlotmonitoritofApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        run = pyre.inventory.facility(
            'instrument', default = "lrmecs" )
        run.meta['tip'] = "The instrument where the experiment is run"

        monitorID = pyre.inventory.int(
            'monitor-id', default = 0 )
        monitorID.meta['tip'] = "id of the beam monitor of interest"

        plotter = pyre.inventory.facility(
            'plotter', default = 'pylabplotter' )

        pass # end of Inventory


    def main(self, *args, **kwds):
        run = self.run
        it = run.getMonitorItof(self.inventory.monitorID )

        plotter = self.plotter
        plotter.interactive( 0 )
        plotter.plot( it )
        return


    def __init__(self):
        Script.__init__(self, 'plotmonitoritof')
        return


    def _configure(self):
        Script._configure(self)
        self.run = self.inventory.run
        self.plotter = self.inventory.plotter
        return


    pass # end of PlotmonitoritofApp



def help( ):
    print 'plotiphi.py: plot I(phi) histogram of a beam monitor of a meausrement'
    print
    print ' $ plotmonitoritof.py -instrument=<instrument name> -<instrument name>.<arg>=<value> ...'
    print
    print ' * Examples:'
    print
    print ' $ plotmonitoritof.py -instrument=lrmecs -lrmecs.filename=4849 -monitor-id=0'
    print
    print ' * Get Help:'
    print
    print ' $ plotmonitoritof.py -instrument=lrmecs -lrmecs.help-properties'
    print


def main():
    import journal
    journal.error( 'pyre.inventory' ).deactivate()
    app = PlotmonitoritofApp()
    try: return app.run()
    except Exception, msg:
        print msg.__class__.__name__, msg
        help()
        return
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
