#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved 
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from reduction.pyre.preprocessors.VPlateDataProcessor import VPlateDataProcessor


import unittestX as unittest

class VPlateDataProcessor_TestCase(unittest.TestCase):

    def test(self):
        testFacility = self

        from pyre.applications.Script import Script

        class Test(Script):

            class Inventory( Script.Inventory ):
                import pyre.inventory
                vdp = pyre.inventory.facility(
                    'vdp', default = VPlateDataProcessor() )
                
                pass # end of Inventory

            def main(self):
                vdp = self.inventory.vdp

                from measurement.ins.Pharos import createVanadiumPlateRun
                r = createVanadiumPlateRun(
                    '../../../ins-data/Pharos/PharosDefinitions.txt',
                    '../../../ins-data/Pharos/Pharos_318.nx.h5' )

                vdp.setInput( 'vanadium', r )

                mask = vdp.getOutput( 'mask' )
                print mask
                return
            
            pass # end of Test

        test = Test('test')
        test.run()
        return
    
    pass # end of VPlateDataProcessor_TestCase


import unittest


def pysuite():
    suite1 = unittest.makeSuite(VPlateDataProcessor_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
    journal.debug('reduction.histCompat').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: VPlateDataProcessor_TestCase.py 1300 2007-07-09 14:14:07Z linjiao $"

# End of file 
