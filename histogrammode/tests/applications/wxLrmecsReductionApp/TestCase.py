#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                     California Institute of Technology
#                   (C) Copyright 2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


hints = '''
Things to try:

  - link: click here for help
  - hover help
  - help button
  - run reductions of 4849 and 5247 (interpolateData=0) (make sure I(tof) plot comes up)
  - save configuration
  - exit
  
'''


import os

def getDataFiles():
    files = [
        "4849",
        ]
    
    dataDir = os.path.join("..", '..', "ins-data", "Lrmecs")
    
    for f in files:
        f = os.path.join( dataDir, f )
        if os.path.exists(  f  ):
            if not os.path.isfile( f ): raise "%s exists but is not a file" % f
            continue
        else:
            raise "%s does not exist" % f
        continue
    return


import unittest

class Tests(unittest.TestCase):

    def __init__(self, *args, **kwds):
        unittest.TestCase.__init__(self, *args, **kwds)
        getDataFiles()
        return
    

    def test1(self):
        "wxLrmecsReductionApp"
        cmd = '''wxLrmecsReductionApp.py'''

        print hints

        import os
        if os.system( cmd ): raise "Failed to execute %s" % cmd
        return

    pass 
        

def pysuite():
    suite1 = unittest.makeSuite(Tests)
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
__id__ = "$Id: LrmecsReductionLight.py 843 2006-04-03 20:38:37Z linjiao $"

# End of file 
