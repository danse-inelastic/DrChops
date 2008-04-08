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


class PlotitofApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        run = pyre.inventory.facility(
            'instrument', default = "lrmecs" )
        run.meta['tip'] = "The instrument where the experiment is run"


        plotter = pyre.inventory.facility(
            'plotter', default = 'pylabplotter' )

        pass # end of Inventory


    def main(self, *args, **kwds):
        run = self.run
        idpt = run.getIdpt( )
        detaxes = idpt.axes()[:-1]

        hist = idpt
        for detaxis in detaxes:
            hist = hist.sum( detaxis.name() )
            continue

        it = hist
        
        plotter = self.plotter
        plotter.interactive( 0 )
        plotter.plot( it )
        return


    def __init__(self):
        Script.__init__(self, 'plotitof')
        return


    def _configure(self):
        Script._configure(self)
        self.run = self.inventory.run
        self.plotter = self.inventory.plotter
        return


    pass # end of PlotitofApp



def help( ):
    print 'plotitof.py: plot I(tof) histogram of a meausrement'
    print
    print ' $ plotitof.py -instrument=<instrument name> -<instrument name>.<arg>=<value> ...'
    print
    print ' * Examples:'
    print
    print ' $ plotitof.py -instrument=lrmecs -lrmecs.filename=4849'
    print ' $ plotitof.py -instrument=pharos -pharos.instrument-definition-filename=PharosDefinitions.txt -pharos.data-filename=Pharos_342.nx.h5'
    print
    print ' * Get Help:'
    print
    print ' $ plotitof.py -instrument=lrmecs -lrmecs.help-properties'
    print ' $ plotitof.py -instrument=pharos -pharos.help-properties'
    print


def main():
    import journal
    journal.error( 'pyre.inventory' ).deactivate()
    app = PlotitofApp()
    try: return app.run()
    except Exception, msg:
        help()
        raise
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
