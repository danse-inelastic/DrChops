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


## \package reduction.pyre.plotter
## provides plotting facility to reduction packages.
## 
## Currently it only has one implementation based on Matplotlib that
## can plot 2D image or contour.
##
## Later this module should be reimplemented once the Graphics API
## is fixed.




from pyre.components.Component import Component



from reduction.utils.plotter import Plotter2D, MplPlotter2D

#pyre components that are simply wrappers

class Plotter2DComp(Component, Plotter2D):

    def __init__(self, name = "Plotter2D", facility = "Plotter"):
        Component.__init__(self, name, facility)
        return

    pass # end of Plotter2DComp


class MplPlotter2DComp( Plotter2DComp, MplPlotter2D):

    def __init__(self, name = "MplPlotter2D"):
        Plotter2DComp.__init__(self, name)
        MplPlotter2D.__init__(self)
        return

    pass # end of MplPlotter2DComp


defaultPlotter2D = MplPlotter2DComp()



from reduction.utils.plotter import Plotter1D, MplPlotter1D

class Plotter1DComp(Component, Plotter1D):

    def __init__(self, name = "Plotter1D", facility = "Plotter"):
        Component.__init__(self, name, facility)
        return

    pass # end of Plotter1DComp


class MplPlotter1DComp( Plotter1DComp, MplPlotter1D):

    def __init__(self, name = "MplPlotter1D"):
        Plotter1DComp.__init__(self, name)
        MplPlotter1D.__init__(self)
        return

    pass # end of MplPlotter1DComp


defaultPlotter1D = MplPlotter1DComp()



# version
__id__ = "$Id: Plot2dHist.py,v 1.4 2005/11/07 23:03:44 linjiao Exp $"

# End of file 
