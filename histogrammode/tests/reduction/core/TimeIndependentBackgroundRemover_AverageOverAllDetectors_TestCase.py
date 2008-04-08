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


from TimeIndependentBackgroundRemover_TestCase import TimeBG_TestCase as Base
import unittestX as unittest


class TimeBG_TestCase(Base):


    from reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors import TimeIndependentBackgroundRemover_AverageOverAllDetectors as Remover 
    

    pass # end of TimeBG_TestCase

    
def pysuite():
    suite1 = unittest.makeSuite(TimeBG_TestCase)
    return unittest.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('Rebinner').activate()
##     journal.debug('instrument').activate()
##     journal.debug('instrument.elements').activate()
##    journal.debug('TBGProcessor').activate()
    journal.debug('BGAccumulator').activate()
##    journal.debug('TBGProcessorPerDet').activate()
##    journal.info('TBGProcessorPerDet').activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
