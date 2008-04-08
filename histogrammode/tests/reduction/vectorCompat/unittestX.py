#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from unittest import *
from unittest import TestCase as TCBase

class TestCase(TCBase):

    def assertAlmostEqual(self, a, b, relativeError = None, epsilon = 1.e-10, **kwds):
        
        if relativeError is None:
            TCBase.assertAlmostEqual( self, a,b,**kwds)
            return

        msg = "%s != %s within relative error %s" % (
            a,b, relativeError )

        if abs(a) < epsilon and abs(b) < epsilon: return
        if abs(a) > epsilon:
            re = abs((b-a)/a)
            if re > relativeError: raise AssertionError , msg
            pass
        else:
            re = abs((a-b)/b)
            if re > relativeError: raise AssertionError , msg
            pass
        return

    def assertVectorEqual( self, v1, v2):
        self.assertEqual( len(v1), len(v2) )
        for x1, x2 in zip(v1, v2): self.assertEqual( x1, x2 )
        return

            
    def assertVectorAlmostEqual( self, v1, v2, *args, **kwds):
        self.assertEqual( len(v1), len(v2) )
        for x1, x2 in zip(v1, v2): self.assertAlmostEqual( x1, x2, *args, **kwds)
        return
            
    def assertMatrixEqual( self, m1, m2):
        self.assertEqual( len(m1), len(m2) )
        for x1, x2 in zip(m1, m2): self.assertVectorEqual( x1, x2 )
        return
            
    def assertMatrixAlmostEqual( self, m1, m2):
        self.assertEqual( len(m1), len(m2) )
        for x1, x2 in zip(m1, m2): self.assertVectorAlmostEqual( x1, x2 )
        return

    pass # end of TestCaae

# version
__id__ = "$Id: unittestX.py 1278 2007-06-23 00:05:54Z linjiao $"

# End of file 
