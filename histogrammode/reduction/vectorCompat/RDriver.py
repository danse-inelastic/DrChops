#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.vectorCompat.RDriver
## driver to add data into S(phi,E) histogram 
##
## The purpose is to add a data vector, which is the intensity(E) array
## for a pixel, to the S(phi,E) histogram. The addition is done
## according to the scattering angle
## of the pixel.

from reduction import reduction as red

from TemplateCObject import TemplateCObject

class RDriver( TemplateCObject):
    
    """Functor for adding vector to S( phi, E) vector"""
    
    def __call__(self, sourceVec, scatteringAngle):
        """rDriver( sourceVector, scatteringAngle) -> None
        add sourceVector's contents to the bin corresponding to scatteringAngle
        Inputs:
            sourceVec: StdVector instance. I(E) for a pixel
            scatteringAngle: angle to add contents of sourceVec to
        Output:
            None
        Exceptions: ValueError, TypeError
        Notes: None"""
        #if sourceVec.datatype() != self._templateType:
        sourceVec = sourceVec.as( vectorType )
        if sourceVec._templateType != self._templateType:
            raise TypeError,'sourceVec datatype does not match this instance'
        red.RDriver_call( self._handle, self._templateType, sourceVec._handle, 
                          scatteringAngle)
        return

    
    def norms(self, destVec = None):
        """norms( destVector) -> None
        return normalization contants as a vector
        Inputs:
            destVec: StdVector instance to save the result. if None, a new vector will be created
        Output:
            the normalization vector
        Exceptions: ValueError, TypeError
        Notes: None"""
        from stdVector import vector
        if destVec is None: destVec = vector( self._templateType, self._len )
        if destVec.datatype() != self._templateType:
            raise TypeError,'destVec datatype does not match this instance'
        red.RDriver_norms( self._handle, destVec._handle, self._templateType )
        return destVec


    def __init__(self, speVec, otherLen, phiBBVec):
        """RDriver( speVector, otherArrLen, phiBBVector)--> RDriver
        Create a new driver object for summing by scattering angle.
        Inputs:
            speVector   (StdVector. 1d vector representing S(phi,E))
            otherArrLen (length of other (non-phi, please think of it as E, the energy)
                         array dimension; int)
            phiBBVector (phi bin boundary vals, degrees; StdVector)
        Output:
            New RDriver instance
        Exceptions: ValueError, TypeError
        Notes: Datatype taken from speVector, datatypes of speVector and
            phiBBVector must match."""
        if speVec.datatype() != phiBBVec.datatype():
            raise TypeError,'speVector and phiBB do not have same datatype'

        self._len = phiBBVec.size()
        
        handle = red.RDriver( speVec._handle, speVec._templateType,\
                                    otherLen, phiBBVec._handle )
        dtype = speVec.datatype()

        # magicNumber 906517712 from RDriver_bdgs.cc
        TemplateCObject.__init__( self, dtype, handle, "Reduction::RDriver",
                                  906517712)
        return 


vectorType = "StdVectorNdArray"


# version
__id__ = "$Id: RDriver.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
