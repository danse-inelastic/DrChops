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

from pyre.components.Component import Component 
from arcseventdata.ParallelHistogrammer import ParallelHistogrammer

class AbstractHistogrammer( Component, ParallelHistogrammer ):


    def __init__(self, name = 'histogrammer', facility = 'histogrammer' ):
        Component.__init__(self, name, facility )
        return
    

    pass # end of AbstractHistogrammer


# version
__id__ = "$Id$"

# End of file 
