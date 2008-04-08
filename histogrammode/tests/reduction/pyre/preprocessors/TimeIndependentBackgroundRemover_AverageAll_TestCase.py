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


import unittest


from TimeIndependentBackgroundRemover_PerDetector_TestCase import TimeIndependentBackgroundRemover_TestCase as base

class TimeIndependentBackgroundRemover_TestCase(base):

    from reduction.pyre.preprocessors.TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as  Remover

    pass

    
def pysuite():
    suite1 = unittest.makeSuite(TimeIndependentBackgroundRemover_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
##     journal.debug('vectorCompat.ERebinAllInOne').activate()
##     journal.debug('Rebinner').activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##     journal.debug('TBGProcessor').activate()
##     journal.debug('BGAccumulator').activate()
##     journal.debug('TBGProcessorPerDet').activate()
##     journal.info('TBGProcessorPerDet').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: TimeIndependentBackgroundRemover_TestCase.py 993 2006-06-29 16:17:55Z linjiao $"

# End of file 
