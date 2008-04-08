#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2005 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## \package reduction.core.AbstractTimeIndependentBackgroundRemover
## Abstract base class for tof-independent background removers.
##
## Removing tof-independent background is an essential step
## in data-preprocessing.
## It removes background that is constant in time, and originates
## mostly from background noise in usual cases.
##
## There can be several different algorithms to do that.
## The simplest algorithm is implemented in
## reduction.core.TimeIndependentBackgroundRemover_AverageOverAllDetectors.
##



class AbstractTimeIndependentBackgroundRemover:

    """
    remove tof-independent background from data

    This is a functor class.

    The method '__call__' will remove time-independent background
    from given hjistograms using a specific algorithm implemented
    in a specific subclass of this class.

    The method '__call__' has following parameters:

     - histograms: a histogram container object. the data to be processed. 
     - mask: the detector mask
    """
    
    def __call__(self, histograms, mask):
        """ remove time-independent background from given histograms"""
        raise NotImplementedError


# version
__id__ = "$Id: TimeBGround.py 1212 2006-11-21 21:59:44Z linjiao $"

# End of file 
