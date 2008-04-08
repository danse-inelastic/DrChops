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



import os
global __file__
curdir = os.path.dirname( __file__ )
ins_data_dir = os.path.join( curdir,  '..', '..', 'ins-data' )
    


import unittestX as unittest
import journal

debug = journal.debug( "VDataProcessor_TestCase" )
warning = journal.warning( "VDataProcessor_TestCase" )


from pyre.units.energy import meV
from pyre.units.length import cm
from pyre.units.angle import degree


import reduction.utils.hpickle as pickle
calibResultsPkl = "vanadiumcalibration-results.pkl"

    

def createProcessor(runFactory, runFactoryArgs, ei = None, whitebeam = None, ):
    from reduction.core.VDataProcessor import VDataProcessor
    
    run = runFactory( *runFactoryArgs )
    
    processor = VDataProcessor(
        run, ei = ei, whitebeam = whitebeam )
    return run, processor


class TestCase(unittest.TestCase):

    def test2(self):
        "VDataProcessor: calibration constants"
        from measurement.ins.Pharos import createVanadiumPlateRun
        pharos_dir = os.path.join( ins_data_dir, 'Pharos' )
        
        datafilename = os.path.join( pharos_dir, 'Pharos_318.nx.h5' )
        instrumentfilename = os.path.join( pharos_dir, 'PharosDefinitions.txt' )

        print "loading data file and create data processor"
        vrun, processor = createProcessor(
            createVanadiumPlateRun,
            (instrumentfilename, datafilename),
            whitebeam = True )

        energy = 70. * meV
        print "computing calibration constants"
        c = processor.calibrationConstants( energy )

        calibresults = pickle.load( calibResultsPkl ) 
        _plot( calibresults )
        return


    def test2a(self):
        "VDataProcessor: calibration constants - Pharos 552"
        from measurement.ins.Pharos import createVanadiumPlateRun
        pharos_dir = os.path.join( ins_data_dir, 'Pharos' )
        datafilename = os.path.join( pharos_dir, 'Pharos_552.nx.h5' )
        instrumentfilename = os.path.join(
            pharos_dir, 'PharosDefinitions.txt' )

        print "loading data file and create data processor"
        vrun, processor = createProcessor(
            createVanadiumPlateRun,
            (instrumentfilename, datafilename),
            whitebeam = True )

        energy = 70. * meV
        print "computing calibration constants"
        if os.path.exists( calibResultsPkl ) : os.remove(calibResultsPkl)
        c = processor.calibrationConstants( energy )
        
        calibresults = pickle.load( calibResultsPkl ) 
        _plot( calibresults )
        return


    def test3(self):
        '''LRMECS run 4779 - whitebeam'''
        from measurement.ins.LRMECS import createVanadiumPlateRun
        lrmecs_dir = os.path.join( ins_data_dir, 'Lrmecs' )
        datafilename = os.path.join( lrmecs_dir, '4779' )

        print "loading data file and create data processor"
        vrun, processor = createProcessor(
            createVanadiumPlateRun, (datafilename, 1), whitebeam = True )

        energy = 70. * meV
        print "computing calibration constants"
        if os.path.exists( calibResultsPkl ) : os.remove(calibResultsPkl)
        c = processor.calibrationConstants( energy )
        
        calibresults = pickle.load( calibResultsPkl ) 
        _plot( calibresults )

        print "computing mask"
        print processor.getMask( energy ).excludedDetectors
        self.assertVectorEqual(
            processor.getMask( energy ).excludedDetectors,
            [32, 34] )
        
        return


    def test4(self):
        '''monochromatic beam calibration
        '''
        from measurement.ins.LRMECS import createVanadiumPlateRun
        lrmecs_dir = os.path.join( ins_data_dir, 'Lrmecs' )
        datafilename = os.path.join(lrmecs_dir, 'V_80meV' )

        print "loading data file and create data processor"
        vrun, processor = createProcessor(
            createVanadiumPlateRun, (datafilename, 0), ei = 80*meV, whitebeam = False )

        cc = processor.calibrationConstants()
        return
    
        
    pass  # end of VDataProcessor_TestCase


def _plot( calibresutls ):
    X, Ys = calibresutls
    xname, x = X
    n = len(Ys)
    import math as m
    ncol = int( m.ceil( m.sqrt(n*1.0) ) )
    nrow = int( m.ceil(1.0*n/ncol))
    import pylab
    pylab.clf()

    import numpy as N
    for plotnum in range( n ):
        pylab.subplot(ncol, nrow, plotnum+1)
        yname, y = Ys[ plotnum ]
        pylab.plot( x, y )
        pylab.xlabel( xname )
        pylab.ylabel( yname )
        ymedian = N.median( y )
        ymax = N.max(y)
        if ymax > ymedian*2: pylab.ylim( 0, ymedian*2 )
        continue
    pylab.show()
    return


def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    #debug.activate()

    #from reduction.core.VDataProcessor import debug
    #debug.activate()

    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    
    
if __name__ == "__main__":
    main()
    
# version
__id__ = "$Id$"

# End of file 
