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
        'normalize_iqe: calcSolidAngleQE'
        from arcseventdata import getinstrumentinfo
        ARCSxml = 'ARCS.xml'
        infos = getinstrumentinfo(ARCSxml)
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        import arcseventdata
        pixelpositions = arcseventdata.readpixelpositions(
            'pixelID2position.bin', npacks, ndetsperpack, npixelsperdet )
                                
        from histogram import axis, arange, histogram
        qaxis = axis( 'Q', arange(0, 13, 0.5), unit = 'angstrom**-1')
        eaxis = axis( 'energy', arange( -50, 50, 5), unit = 'meV' )
        sa = histogram( 'solid angle', [qaxis, eaxis] )
        
        ei = 70
        from arcseventdata.normalize_iqe import calcSolidAngleQE
        calcSolidAngleQE(sa, ei, pixelpositions)

        from histogram.plotter import defaultPlotter
        defaultPlotter.plot( sa )
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
