#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class DivErrorPropagator( object):

    def propagate( self, x, sigma_x2, y, sigma_y2, output,
                   tempVector = None):  #,
        #tempYVector2 = None):
        """Propagate errors for array x divided by array y.
        y's elements must be non-zero.
        <formula>sigma_f^2 = y^{-4}*sigma_y^2*x^2 + y^{-2}*sigma_x^2</formula>
        Inputs:
            x: vector that was divided by a
            sigma_x2: squares of errors associated with x, same type & length
                      as x
            y: non-zero array
            sigma_y2: non-zero squared errors for y
            output: vector in which to place output. 
            tempVector: vector in which to do some work. Must be same size as
                        x and sigma_x2. If None, this function will allocate
                        temp space.
        Output:
            output
        Exceptions:
        Notes: You must not pass either x or y as the output vector."""
        import stdVector

        #keep a copy if necessary (for example x/=y)
        if sigma_x2 == output: sigma_x2 = stdVector.copy( sigma_x2 )
        if sigma_y2 == output: sigma_y2 = stdVector.copy( sigma_y2 )
         
        output.assign( y.size(), 1.0)
        output.divideEquals( y)
        output.square()

        if tempVector:
            temp_x2 = tempVector
        else:
            temp_x2 = stdVector.vector( x.datatype(), x.size())
        stdVector.square( x, temp_x2)
        temp_x2.timesEquals( sigma_y2)
        temp_x2.timesEquals( output)
        temp_x2.timesEquals( output)

        output.timesEquals( sigma_x2)

        output.plusEquals( temp_x2)

        return output

    
# version
__id__ = "$Id: DivErrorProp.py 721 2005-12-08 17:40:09Z linjiao $"

# End of file
