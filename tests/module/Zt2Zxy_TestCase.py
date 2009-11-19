#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                         (C) 2009 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import drchops.drchops as red

import unittestX as ut


class TestCase(ut.TestCase):

    def test(self):
        "Zt2Zxy"

        nx = 10
        ny = 15
        nt = 1000
        
        
        from numpy import array, arange, ones, zeros, sum
        xt = arange(nt, dtype='d')/100.
        yt = arange(nt, dtype='d')**2/50000
        zt = ones(nt, dtype='d')
        mask = zeros(nt, dtype='i')

        xbb = arange(nx, dtype='d')
        ybb = arange(ny, dtype='d')
        z = zeros((nx-1,ny-1), dtype='d')

        print "finished initialization of data, start reduction..."
        red.Zt2Zxy_numpyarray(
            xt, yt, zt, mask,
            xbb, ybb, z)

        print "reduction done."
        print z
        return
    
    pass # end of TestCase



def pysuite():
    suite1 = ut.makeSuite(TestCase)
    return ut.TestSuite( (suite1,) )

def main():
    import journal
    journal.debug('reduction.Universal1DRebinner').activate()
    pytests = pysuite()
    alltests = ut.TestSuite( (pytests, ) )
    ut.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id$"

# End of file 
