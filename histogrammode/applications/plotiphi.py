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


class PlotiphiApp(Script):


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
        idet = idpt.sum( 'tof' ).sum( 'pixelID' )

        detaxes = idet.axes()

        from reduction.core.getDetectorInfo import getScatteringAngles

        instrument, geometer = run.getInstrument()

        phidet = getScatteringAngles(instrument, geometer, detaxes)

        phis = phidet.data().storage().asNumarray()
        intensities = idet.data().storage().asNumarray()

        o = phis.argsort()
        phis = phis[o]
        intensities = intensities[o]

        #some phi angles in the "phis" array might be equal to each other,
        #because detectors in the "ring" that is circularly symetric
        #about the z axis all scattering angles are equal.
        #we cannot create histogram unless we do reduction, in this case.
        #so the following code does not work:
        #
        #from histogram import histogram
        #h = histogram('h', [('phi', phis)], data = intensities )
        #plotter = self.plotter
        #plotter.interactive( 0 )
        #plotter.plot( h )
        #
        #instead, we can plot by simply using pylab
        import pylab
        pylab.plot( phis, intensities )
        pylab.show()
        return


    def __init__(self):
        Script.__init__(self, 'plotiphi')
        return


    def _configure(self):
        Script._configure(self)
        self.run = self.inventory.run
        self.plotter = self.inventory.plotter
        return


    pass # end of PlotiphiApp



def help( ):
    print 'plotiphi.py: plot I(phi) histogram of a meausrement'
    print
    print ' $ plotiphi.py -instrument=<instrument name> -<instrument name>.<arg>=<value> ...'
    print
    print ' * Examples:'
    print
    print ' $ plotiphi.py -instrument=lrmecs -lrmecs.filename=4849'
    print ' $ plotiphi.py -instrument=pharos -pharos.instrument-definition-filename=PharosDefinitions.txt -pharos.data-filename=Pharos_342.nx.h5'
    print
    print ' * Get Help:'
    print
    print ' $ plotiphi.py -instrument=lrmecs -lrmecs.help-properties'
    print ' $ plotiphi.py -instrument=pharos -pharos.help-properties'
    print


def main():
    import journal
    journal.error( 'pyre.inventory' ).deactivate()
    app = PlotiphiApp()
    try: return app.run()
    except Exception, msg:
        print msg.__class__.__name__, msg
        help()
        raise
        return
    return


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
