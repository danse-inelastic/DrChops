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


from pyre.units.energy import meV


import unittest


from unittestX import TestCase
class Spe2Sqe_TestCase(TestCase):


    def test(self):
        """
        """
        intensity_scale = 3.

        #prepare data
        from histogram import axis, histogram, arange, datasetFromFunction
        phiAxis = axis( 'phi', boundaries = arange( 0., 120., 5. ), unit = 'degree'  )
        EAxis = axis( 'energy', arange( -50, 50, 5.), unit='meV' )

        axes = phiAxis, EAxis
        spe = histogram('spe', axes )

        def f(phi): return 1+0.*phi
        spe[ (), 0. ] = datasetFromFunction(f, (phiAxis,)), datasetFromFunction(f, (phiAxis,))

        spe *= intensity_scale, 0 # to test handling of unit

        from reduction.core.Spe2Sqe import spe2sqe

        QAxis = axis( 'Q', arange(0.,13.,0.5), 'angstrom**-1' )

        ei = 60. * meV
        
        sqe = spe2sqe( ei, spe,  QAxis)

        pickle.dump(sqe, open('sqe.pkl','w') )
                
        #compare reduced data to direct computatiion
        self._check(spe, ei, QAxis, sqe)
        return


    def oracle(self, spe, ei, QAxis):
        global spe2sqe
        return spe2sqe( spe, ei, QAxis )


    def _check(self, spe, ei, QAxis, sqe):
        sqe1 = self.oracle( spe, ei, QAxis )
        pickle.dump(sqe1, open('sqe1.pkl','w') )
        return
            
    pass # end of Spe2Sqe_TestCase



def spe2sqe( spe, ei, QAxis ):
    ei = ei/meV
    
    from reduction.utils.conversion import k2e, e2k
    ki = e2k( ei )
    ki2 = ki*ki

    from numpy import cos, sin, sqrt, pi
    deg2radian = pi/180.
    
    def kf_( E ):
        return e2k( ei - E )
        
    def Q_( phi,E ):
        phi = phi*deg2radian
        kf = kf_(E)
        Q2 = ki2 + kf*kf -2*ki*kf*cos(phi)
        return sqrt(Q2)

    epsilon = 1.e-10 # to avoid singularity
    def J( phi, E ):
        phi = phi*deg2radian
        return ki * kf_(E) * (sin(phi)+epsilon) / Q_(phi,E)

    phiAxis = spe.axisFromName( 'phi' )
    EAxis = spe.axisFromName( 'energy' )

    from histogram import histogram, datasetFromFunction
    Jacobians = histogram( 'Jacobians', [phiAxis, EAxis] )
    Jacobians[(),()] = datasetFromFunction( J, [phiAxis, EAxis] ), None

    sqe = histogram( 'sqe', [QAxis, EAxis] )
    
    from reduction.histCompat.Rebinner import rebinner
    def QE_( phiE ):
        phi,E = phiE
        Q = Q_(phi,E)
        return Q,E
        
    rebinner.rebin( spe, sqe, QE_, Jacobians)
    return sqe


import pickle    
    

import unittest

def pysuite():
    suite1 = unittest.makeSuite(Spe2Sqe_TestCase)
    return unittest.TestSuite( (suite1,) )



def main():
    import journal
    ##     journal.debug('Rebinner').activate()
    #journal.debug('Spe2Sqe_TestCase').activate()
    #journal.debug('Spe2Sqe').activate()
    #journal.debug('Rebinner').activate()
    #journal.debug("NdArrayDataset").activate()
    pytests = pysuite()
    alltests = unittest.TestSuite( (pytests, ) )
    unittest.TextTestRunner(verbosity=2).run(alltests)
    return


if __name__ == '__main__': main()
    

# version
__id__ = "$Id: Spe2Sqe_TestCase.py 1264 2007-06-04 17:56:50Z linjiao $"

# End of file 
