# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component
from arcseventdata.parallel_histogrammers.IhkleHistogrammer import IhkleHistogrammer as base

class IhkleHistogrammer( Component, base ):


    def __init__(self, name = 'histogrammer', facility = 'histogrammer' ):
        Component.__init__(self, name, facility )
        return
    

    pass # end of IhkleHistogrammer



# version
__id__ = "$Id$"

# End of file 
