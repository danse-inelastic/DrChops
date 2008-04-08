#!/usr/bin/env python
# Jiao Lin Copyright (c) 2006 All rights reserved

class Normalizer( object):

    def normalize( self, dataset, outputDataset, error, outputError,
                   tempVector = None):
        """normalize( dataset, outputDataset, error, outputError,
                      tempVector = None) -> (outputDataset, outputError)
        Multiply each element of dataset by 1.0/norm.
        Inputs:
            dataset: data to normalize
            outputDataset: output vector for scaled data
            error: vector with errors
            outputError: output for scaled errors
            tempVector: temporary vector, same size as dataset.
        Output: (outputDataset, outputError)
        Exceptions:
        Notes:
            (1) In order to change dataset (errors) in place, simply pass
                dataset (errors) in both the dataset and outputDataset slots
                (errors and outputErrors slots).
            (2) If outputError is None, no error propagation will be performed.
            (3) If no tempVector is supplied, one will be allocated by the
                errorPropagator. This is slow, so if this gets used a lot,
                consider supplying your own."""
        # dataset must provide multScalar method, as per StdVector
        # propagate errors first, since requires original data values
        if outputError:
            self._errorProp.propagate( dataset, error, self._norm,
                                       self._sigma2, outputError, tempVector)

        normRecip = 1.0/self._norm
        dataset.multScalar( normRecip, outputDataset)

        return (outputDataset, outputError)


    def norm( self):
        """norm() -> present value of norm"""
        return self._norm


    def sigma_norm2( self):
        """square of error associated with norm"""
        return self._sigma2


    #default error propagator
    from DivScalarErrorProp import DivErrorPropagator
    _errorProp = DivErrorPropagator()


    def __init__(self, norm, sigma_norm2):
        self._norm = norm
        self._sigma2 = sigma_norm2
        return


    pass # end of Normailzer



# version
__id__ = "$Id: Normalizer.py 576 2005-07-26 23:02:02Z tim $"

# End of file
