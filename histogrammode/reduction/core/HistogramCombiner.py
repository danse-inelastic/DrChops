#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

## \package reduction.core.HistogramCombiner
## Provides a calculator that combines histograms.
## The input 
## is a list of (counts, jacobians).
## Read the documentation for the class for more details.



class HistogramCombiner:

    '''In the traditional way of reduction, when histograms are
    converted to new coordinates, Jacobians are also acummulated
    in the new grid. Let us use S(Q,E) as example

    S(Q,E) = cnts(Q,E) / J(Q,E)

    When we combine histograms from several sources, we may want
    to combine them carefully:

    S(Q,E) = (cnts1(Q,E)+cnts2(Q,E)/(J1(Q,E)+J2(Q,E)

    This combiner is only needed for "rebiner"-based reduction.
    For interpolation-based reduction, it is not necessary.
    '''

    def __call__(self, counts_and_Jacobians ):
        '''combine histograms by doing things similar to
        
    S(Q,E) = (cnts1(Q,E)+cnts2(Q,E)/(J1(Q,E)+J2(Q,E)

    Inputs:
      counts_and_Jacobians: list of (counts, Jacobians) tuple
    '''
        totcounts, totJacobians = counts_and_Jacobians[0]
        
        for counts, Jacobians in counts_and_Jacobians[1:]:
            totcounts += counts
            totJacobians += Jacobians
            continue

        return totcounts/totJacobians

    pass # end of HistogramCombiner



def combine( counts_and_Jacobians ):
    combiner = HistogramCombiner()
    return combiner( counts_and_Jacobians )


# version
__id__ = "$Id$"

# End of file 
