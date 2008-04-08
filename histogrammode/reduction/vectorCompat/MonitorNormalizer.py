#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat.MonitorNormalizer
## normalize datasets by monitor counts

class MonitorNormalizer( object):
    
    """Find norms from monitor data, and normalize datasets by it"""
    
    def determineNorm( self, monitorData, start, end, dt):
        """determineNorm( monitorData, start, end, dt) -> None
        Determine the normalization factor from a given monitor data set by
        integrating over the range from start to but not including end with
        bin size dt.
        Inputs:
            monitorData: vector of monitor data (counts)
            start, end: channel range over which to integrate
            dt: bin size (float)
        Output:
            None (result stored in this object for later use.
        Exceptions: ValueError, IndexError
        Notes: raises ValueError if norm is equal to 0.0. Other exceptions
        raised in monitorData.integrate"""
        self._norm = monitorData.integrate( start, end, dt)
        
        if self._norm == 0.0:
            msg = "norm is zero: will generate inf's"
            raise ValueError, msg
        
        self._sigma2 = self._norm*dt

        return


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


    def __init__( self, *args, **kwds):
        """MonitorNormalize( **kwds)"""
        # optional keyword arg: errorPropagator: functor that propagates errors
        # if not supplied, defaults to DivErrorProp.ErrorPropagator
        if 'errorPropagator' in kwds:
            errorProp = kwds['errorPropagator']
        else:
            from DivScalarErrorProp import DivErrorPropagator
            errorProp = DivErrorPropagator()
        self._errorProp = errorProp
        return


# version
__id__ = "$Id: MonitorNormalizer.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
