# -*- Python -*-
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


from pyre.components.Component import Component
from arcseventdata.parallel_histogrammers.IqqqeHistogrammer import IqqqeHistogrammer as base

class IqqqeHistogrammer( Component, base ):


    def __init__(self, name = 'histogrammer', facility = 'histogrammer' ):
        Component.__init__(self, name, facility )
        return
    

    pass # end of AbstractHistogrammer



# version
__id__ = "$Id$"

# End of file 
