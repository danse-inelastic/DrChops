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


import unittest

from unittest import TestCase
class TestCase(TestCase):


    def test1(self):
        'normalize_iqqqe: calcSolidAngleQQQE'
        from arcseventdata import getinstrumentinfo
        ARCSxml = 'ARCS.xml'
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        import arcseventdata
        pixelpositions = arcseventdata.readpixelpositions(
            'pixelID2position.bin', npacks, ndetsperpack, npixelsperdet )
                                
        from histogram import axis, arange, histogram
        qxaxis = axis( 'Qx', arange(-10, 10, 1), unit = 'angstrom**-1')
        qyaxis = axis( 'Qy', arange(-10, 10, 1), unit = 'angstrom**-1')
        qzaxis = axis( 'Qz', arange(-10, 10, 1), unit = 'angstrom**-1')
        eaxis = axis( 'energy', arange( -50, 50, 5), unit = 'meV' )
        sa = histogram( 'solid angle', [qxaxis, qyaxis, qzaxis, eaxis] )
        
        ei = 70
        pixel_area = 0.025*1./128
        from arcseventdata.normalize_iqqqe import calcSolidAngleQQQE
        calcSolidAngleQQQE(sa, ei, pixel_area, pixelpositions)

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( sa.sum('Qz').sum('energy') )
        return
    
    
    pass # end of TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: TestCase.py 1124 2006-09-05 23:08:19Z linjiao $"

# End of file 
