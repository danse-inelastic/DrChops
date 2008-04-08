#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class MultErrorPropagator( object):


    def propagate( self, x, sigma_x2, y, sigma_y2, outputVector,
                   tempVector = None):
        """propagate( x, sigma_x2, y, sigma_y2, outputVector,
                      tempXVector = None, tempYVector = None) -> outputVector
        Propagate errors for array x multiplied by array y.
        <formula>sigma_f^2 = x^2*sigma_y^2 + y^{2}*sigma_x^2</formula>
        Inputs:
            x: vector that was divided by a
            sigma_x2: squares of errors associated with x, same type & length
                      as x
            y: non-zero vector
            sigma_y2: non-zero squared error for y, (scalar)
            outputVector: vector in which to place output. 
            tempVector: vector in which to do some work. Must be same size as
                x. If None, this function will allocate temp space.
        Output:
            outputVector
        Exceptions: ValueError
        Notes: (1) allocating the temp vector will decrease performance, so
        only use on this allocation if you're trying something quick.
        (2) You can pass y as the output vector, but not x."""

        import stdVector
        #keep a copy if necessary (for example x*=y)
        if sigma_x2 == outputVector: sigma_x2 = stdVector.copy( sigma_x2 )
        if sigma_y2 == outputVector: sigma_y2 = stdVector.copy( sigma_y2 )

        # prepare copy of x, square it, multiply be y errors^2
        import stdVector
        if tempVector:
            temp_x2 = tempVector
        else:
            temp_x2 = stdVector.vector( x.datatype(), x.size())

        stdVector.square( x, temp_x2)
        temp_x2.timesEquals( sigma_y2)

        # use output as temp_y2:
        stdVector.square( y, outputVector)
        outputVector.timesEquals( sigma_x2)

        outputVector.plusEquals( temp_x2)

        return outputVector

        
# version
__id__ = "$Id: MultErrorProp.py 721 2005-12-08 17:40:09Z linjiao $"

# End of file
