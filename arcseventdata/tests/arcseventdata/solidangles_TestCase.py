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
        ARCSxml = 'ARCS.xml'
        
        from instrument.nixml import parse_file
        arcs = parse_file( ARCSxml)

        import arcseventdata
        infos = arcseventdata.getinstrumentinfo( ARCSxml )
        npacks, ndetsperpack, npixelsperdet = infos[
            'detector-system-dimensions']
        pixelPositionsFilename = infos[
            'pixelID-position mapping binary file']
        pixelPositions = arcseventdata.readpixelpositions(
            pixelPositionsFilename, npacks, ndetsperpack, npixelsperdet)
        
        from arcseventdata.solidangles import solidangles
        
        sas = solidangles(
            pixelPositions, arcs,
            npixelsperdet, ndetsperpack, npacks)

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
