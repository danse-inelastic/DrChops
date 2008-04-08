#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class AdditionErrorPropagator( object):

    def propagate( self, errVect, sigma_a2, outputVect = None):
        """propagate( errVect, sigma_a2, outputVect = None)
        Propagate errors from adding a scalar "a" with squared error sigma_a2
        to an array with errors given by errVect, placing the results in
        outputVect; if not outputVect is given, results are placed in errVect.
        Inputs:
            errVect: StdVector instance with """
        if not outputVect:
            outputVect = errVect

        errVect.addScalar( sigma_a2, outputVector = outputVect)

        return outputVect


    def __init__( self, *args, **kwds):
        return

    
# version
__id__ = "$Id: AddScalarErrorProp.py 438 2005-05-19 14:40:49Z tim $"

# End of file
