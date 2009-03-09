#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

'''
To run this test in parallel, you can run

 $ mpirun -n 8 `which mpipython.exe` ReduceToMslice_TestCase.py

'''


try:
    import mpi
    mpiRank = mpi.world().rank
except ImportError:
    mpiRank = 0


import unittest

from unittestX import TestCase as base
class TestCase(base):


    def _test0(self):
        ARCSxml = 'ARCS.xml'
        
        from arcseventdata import getinstrumentinfo
        ii = getinstrumentinfo(ARCSxml)
        detaxes = ii['detector axes']
        
        import histogram as H
        Eaxis = H.axis('energy', H.arange(-50,50,20))

        axes = detaxes + [Eaxis]
        ipdpE = H.histogram('I(pdpE)', axes)
        
        from reduction.core.ARCS.ReduceToMslice import write_mslice_files
        outputprefix = 'mslice'
        write_mslice_files(
            outputprefix, ipdpE, ARCSxml, (1,115), 1)
        return
    

    def _test0a(self):
        ARCSxml = 'ARCS.xml'
        
        import histogram as H
        from arcseventdata import getinstrumentinfo
        ii = getinstrumentinfo(ARCSxml)
        detaxes = ii['detector axes']
        pixelaxis = H.axis('pixelID', H.arange(1, 128, 2.))
        detaxes[-1] = pixelaxis
        
        Eaxis = H.axis('energy', H.arange(-50,50,20))

        axes = detaxes + [Eaxis]
        ipdpE = H.histogram('I(pdpE)', axes)
        
        from reduction.core.ARCS.ReduceToMslice import write_mslice_files
        outputprefix = 'mslice'
        write_mslice_files(
            outputprefix, ipdpE, ARCSxml, (1,115), 2)
        return


    def test1(self):
        'no calibration, no mask, no empty can data'
        mainrun = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_279'
        inputs = [
            mainrun,
            ]

        outputprefix = 'mslice-nocali-nomask-nomt'
        outputs = _mslice_outputs( outputprefix )
        
        for inputdir in inputs:
            assert os.path.exists( inputdir  )
            continue
        
        for output in outputs:
            if os.path.exists( output ): os.remove( output )
            continue

        mslice = reduce(
            mainrun,
            Ei = 100,
            E_params = (-90,90,1.),
            outputprefix = outputprefix,
            )
        return

    def _test2(self):
        'no calibration, no mask. with empty can data'
        mainrun = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_279'
        mtrun = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_289'
        inputs = [
            mainrun,
            mtrun,
            ]

        outputprefix = 'mslice-nocali-nomask-mtsubtracted'
        outputs = _mslice_outputs( outputprefix )
        
        for inputdir in inputs:
            assert os.path.exists( inputdir  )
            continue
        
        for output in outputs:
            if os.path.exists( output ): os.remove( output )
            continue
        
        reduce(
            mainrun,
            mtrundir = mtrun,
            Ei = 100,
            E_params = (-90,90,1.),
            outputprefix = outputprefix,
            )
        return

    def _test3(self):
        'do calibration. use mask. use empty can data'
        mainrun = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_279'
        mtrun = '/ARCS-DAS-FS/2008_2_18_SCI/ARCS_289'
        calibration_constants_input = 'calibration.h5'
        mask_input = 'mask.h5'
        inputs = [
            mainrun,
            mtrun,
            calibration_constants_input,
            mask_input,
            ]

        outputprefix = 'mslice-calibrated-masked-mtsubtracted'
        outputs = _mslice_outputs( outputprefix )
        
        for inputdir in inputs:
            assert os.path.exists( inputdir  )
            continue
        
        for output in outputs:
            if os.path.exists( output ): os.remove( output )
            continue

        calibration = hdf.load( calibration_constants_input, 'calibration' )
        mask = hdf.load( mask_input, 'mask' )
        reduce(
            mainrun,
            mtrundir = mtrun,
            Ei = 100,
            E_params = (-90,90,1.),
            calibration = calibration,
            mask = mask,
            outputprefix = outputprefix,
            )
        return

    pass # end of TestCase


def _mslice_outputs( prefix ):
    return [
        '%s.spe'%prefix,
        '%s.phx'%prefix,
        '%s-IpdpE.h5'%prefix,
        ]

from histogram import hdf
import os
from reduction.core.ARCS.ReduceToMslice import reduce, info
info.activate()
from histogram.plotter import defaultPlotter


import reduction.units as units


import unittest

def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    from reduction.core.ARCS.ReduceToMslice import debug
    debug.activate()
    
    import journal
    #journal.debug('reduction.core.getPixelInfo' ).activate()
    journal.info('histogrammer' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
