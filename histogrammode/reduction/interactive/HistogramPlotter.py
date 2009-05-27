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


from FacilityFrontEnd import *

class HistogramPlotter(FacilityFrontEnd):
    
    engineFactories = FacilityFrontEnd.engineFactories.copy()
    interface = [
        '__call__',
        'interactive',
        ]
    onelinehelp = 'Plot histogram'
    pass


plot = HistogramPlotter()


from histogram.plotter import HistogramMplPlotter as _Plotter
class Plotter(_Plotter):
    def __call__(self, *args, **kwds):
        'plot( histogram ): new plot of a histogram'
        _Plotter.plot( self, *args, **kwds )
        return
    __call__.__doc__ = _Plotter.plot.__doc__
    pass # end of Plotter

plot.registerEngineFactory('pylab',  Plotter)


plot.select( 'pylab' )


__all__ = ['HistogramPlotter', 'plot']



# version
__id__ = "$Id$"

# End of file 
