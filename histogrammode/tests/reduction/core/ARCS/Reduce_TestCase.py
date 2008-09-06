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

 $ mpirun -n 8 `which mpipython.exe` Reduce_TestCase.py

'''


try:
    import mpi
    mpiRank = mpi.world().rank
except ImportError:
    mpiRank = 0


import unittest

from unittestX import TestCase as base
class TestCase(base):

    def test(self):
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

        spe_output = 'spe.h5'
        outputs = [
            spe_output,
            ]
        
        import os
        for inputdir in inputs:
            assert os.path.exists( inputdir  )
            continue
        
        for output in outputs:
            if os.path.exists( output ): os.remove( output )
            continue
        
        from reduction.core.ARCS.Reduce import reduce
        spe = reduce(
            mainrun,
            Ei = 100,
            tof_params = (3000,6000,5.),
            E_params = (-90,90,1.),
            nodes = 8,
            )
        
        from histogram.hdf import dump
        dump( spe, spe_output, '/', 'c' )

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( spe )
        return

    pass # end of TestCase


import reduction.units as units


import unittest

def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    #journal.debug('reduction.core.getPixelInfo' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
