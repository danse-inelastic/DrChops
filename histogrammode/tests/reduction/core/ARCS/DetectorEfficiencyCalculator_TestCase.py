#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import unittest


from unittestX import TestCase as base
class TestCase(base):

    interactive = False

    def test1(self):
        """DetectorEfficiencyCalculator: one energy value
        """
        from reduction.core.ARCS.DetectorEfficiencyCalculator import deteff_hist
        import reduction.units as units
        meV = units.energy.meV
        energy = 70*meV
        eff = deteff_hist(energy)

        from arcseventdata import detectorview
        v = detectorview(eff, averagingShortTubes=1)
        
        if self.interactive:
            from histogram.plotter import defaultPlotter
            defaultPlotter.plot(v)
        return
        

    def test2(self):
        """DetectorEfficiencyCalculator: energy axis
        """
        from reduction.core.ARCS.DetectorEfficiencyCalculator import deteff_hist
        import histogram 
        energyAxis = histogram.axis('energy', histogram.arange(30,100,1), 'meV')
        eff = deteff_hist(energyAxis)

        import histogram.hdf as hh
        filename = 'efficiency.h5'
        import os
        if os.path.exists(filename): os.remove(filename)
        hh.dump(eff, filename, '/', 'c')

        if self.interactive:
            # sum over pixels
            effpde = eff.sum('pixelID')
        
            from histogram.plotter import defaultPlotter
            defaultPlotter.plot(effpde[{'detectorpackID':1}])
            import pylab
            pylab.colorbar()
        return
        
    pass # end of TestCase


import reduction.units as units


import unittest

def pysuite():
    TestCase.interactive = True
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    journal.debug('reduction.core.getPixelInfo' ).activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
