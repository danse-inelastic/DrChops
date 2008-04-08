#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 T. M. Kelley
#                   (C) Copyright 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
"""
reduce powder data from ARCS instrument simulation

    - NAME:
      ARCSReduction

    - PURPOSE:
      reduce powder data from ARCS instrument simulation
      This application corrects data up to S(phi, E).

    - DESCRIPTION:
      This is a pyre application used to reduce ARCS simulation data.
"""

from pyre.applications.Script import Script

from math import sqrt, ceil

import cPickle, numpy as N
import pylab
try: pylab.show()
except: pass

import journal
warning = journal.warning( "ARCSSimuReduction")
warning.activate()



class PowderreductionApp(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory  as inv

        # ------------------------- facilities: ---------------------------

        # measurement
        measurement = inv.facility("Measurement", default = "ARCSSimuMeasurement")
        measurement.meta['tip'] = "provides histograms"

        # incident energy solver
        e_iSolver = inv.facility( "IncidentEnergySolver", default = "ARCSSimuIncidentEnergySolver")
        e_iSolver.meta['tip'] = "determines incident energy"

        # main data extractor
        mainDataExtractor = inv.facility("MainDataExtractor", default = "ARCSSimuMainDataExtractor")
        mainDataExtractor.meta['tip'] = "extract main data from measurment"

        # reducer to reduce data to s(phi,E)
        speReducer = inv.facility("SpeReducer", default = "ARCSSimuSpeReducer")
        speReducer.meta['tip'] = "reducer to reduce data to s(phi,E)"

        # plotter
        from graphics.Matplotlib import pylab
        plotter = inv.facility( "matplotlib", factory=pylab)

        # --------------------------- end of inventory ------------------------


    def preMain(self):
        """If run this application from python interactive environment,
        run this method first before running main()
        """
        #these codes are copied from pyre.Application.Application.run
        #they initialize the components tree and apply configurations
        #only after these steps are done, this application is ready to run
        self.registry = registry = self.createRegistry()
        curator = self.createCurator()
        self.initializeCurator(curator, registry)
        self.initializeConfiguration()
        self.updateConfiguration(registry)
        unknowns = self.applyConfiguration()
        self.init()
        return


    def postMain(self):
        """If run this application from python interactive environment,
        run this method after running main()
        """
        self.fini()
        return
    

    def main(self, *args, **kwds):
        measurement = self.measurement

        # prepare
        ei = self.e_iSolver.solve( measurement)
        print "* Incident energy is %s" % ei


        # 4. prepare vectors for tof and pixel storage
        # aaagh--forgot it takes HDF forever to read slices. So, read whole
        # thing, use extractSlice to pull out small chunks.
        mainDataSet = self.mainDataExtractor.extract( measurement )
        

        # 5,6. reduce to s(phi,E)
        print "* Reduce data to s(phi,E)"
        sphiEHist = self.speReducer( mainDataSet, ei, measurement)
        
        
        # 7. loop over phis, converting to S(|Q|, E)
        #sQEHist = self.Spe2Sqe(ei, sphiEHist)

        ## conclude
        #raw_input("-- Press ENTER to conclude")
        return


    def __init__(self):
        Script.__init__(self, 'ARCSSimuReduction')
        return


    def _defaults(self):
        Script._defaults(self)
        return


    def _configure(self):

        Script._configure(self)

        si = self.inventory   # handy alias

        # transcribe components
        self.measurement = si.measurement
        self.e_iSolver = si.e_iSolver
        self.mainDataExtractor = si.mainDataExtractor
        self.speReducer = si.speReducer

        self.plotter = si.plotter
        
        return


    def _init(self):
        Script._init(self)
        return



# main
if __name__ == '__main__':
    # invoke the application shell
    app = PowderreductionApp()
    #app._info.activate()
    #app._debug.activate()

    import journal, sys, profile
##     journal.debug( "measurement.ARCSMeasurement").activate()
##     journal.debug("histogram.DetPackData").activate()
    
    # profile?
    if 'profile' in sys.argv:
        profile.run( 'app.run()', 'profPowRed.txt')
    else:
        app.run()

    import os
    print "times: %s" % str(os.times())

# version
__id__ = "$Id: PowderReduction.py 1059 2006-08-04 20:06:27Z linjiao $"

# Generated automatically by PythonMill on Wed Jul 13 16:55:30 2005

# End of file 
