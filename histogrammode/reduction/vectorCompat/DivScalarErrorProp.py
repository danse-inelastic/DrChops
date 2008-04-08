#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class DivErrorPropagator( object):

    def propagate( self, x, sigma_x2, a, sigma_a2, outputVector = None,
                   tempVector = None):
        """Propagate errors for array x divided by scalar a.
        a must be non-zero.
        <formula>sigma_f^2 = a^{-4}*sigma_a^2*x^2 + a^{-2}*sigma_x^2</formula>
        Inputs:
            x: vector that was divided by a
            sigma_x2: squares of errors associated with x, same type & length
                      as x
            a: non-zero scalar
            sigma_a2: non-zero squared error for a, (scalar)
            outputVector: vector in which to place output. If None, output
                          placed in sigma_x2.
            tempVector: vector in which to do some work. Must be same size as
                        x and sigma_x2. If None, this function will allocate
                        temp space
        Output:
            outputVector if outputVector was not None, otherwise sigma_a2
            """
        a4 = 1.0/a**4
        a2 = 1.0/a**2
        
        import stdVector
        if tempVector:
            temp_x2 = tempVector
        else:
            temp_x2 = stdVector.vector( x.datatype(), x.size())

        stdVector.square( x, temp_x2)
        temp_x2.multScalar( a4*sigma_a2)

        retval = None
        
        if outputVector:
            sigma_x2.multScalar( a2, outputVector = outputVector)
            outputVector.plusEquals( temp_x2)
            retval = outputVector
            
        else:
            sigma_x2.multScalar( a2)
            sigma_x2.plusEquals( temp_x2)
            retval = sigma_x2
            
        return retval

    
# version
__id__ = "$Id: DivScalarErrorProp.py 438 2005-05-19 14:40:49Z tim $"

# End of file
