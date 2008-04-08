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

from reduction.pyre.preprocessors.NormalizerUsingMonitorData import NormalizerUsingMonitorData as NormalizerBase

class Normalizer(NormalizerBase):

    def _defaults(self):
        NormalizerBase._defaults(self)
        self.inventory.tofStart = 201
        self.inventory.tofEnd = 399
        return
    pass # end of Class Normalizer
    



from NormalizerUsingIntegratedCurrent_TestCase import Normalizer_TestCase as Base

class Normalizer_TestCase(Base):

    def __init__(self, *args, **kwds):
        Base.__init__(self, *args, **kwds)
        self.Normalizer = Normalizer
        from measurement.ins.Fake.Run import integratedMonitorIntensity
        self.norm = integratedMonitorIntensity
        return

    
    pass # end of Normalizer_TestCase


import unittest


def pysuite():
    suite1 = unittest.makeSuite(Normalizer_TestCase)
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
__id__ = "$Id: NormalizerUsingMonitorData_TestCase.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file 
