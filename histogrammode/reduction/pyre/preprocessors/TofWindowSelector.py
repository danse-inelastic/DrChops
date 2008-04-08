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


from Connectable import Connectable as base

class TofWindowSelector(base):


    '''Time-of-flight window selector

    To remove time-independent background, the simpliest way to do that
    is to pick a window on tof axis, compute the average counts in that
    window, and remove the average from all pixel. This component
    plots the I(tof) curve and let you choose the tof window.
    '''


    sockets = {
        'in': ['Idpt'],
        'out': ['tofWindow'],
        }


    def _update(self):
        Idpt = self._getInput( 'Idpt' )
        Itof = Idpt.sum('detectorID').sum('pixelID' )
        x = Itof.axisFromName('tof').binCenters()
        y = Itof.data().storage().asNumarray()
        tofWindow = self._plot_xy( x, y )
        self._setOutput( 'tofWindow', tofWindow )
        return


    def __init__(self, name='Preprocess_TofWindowSelector' ):
        base.__init__(self, name, facility = 'facility')
        return
    

    def _plot_xy(self, x,y):
        #this implementation uses wxmpl. This is a quick solution.
        app = PlotApp(
            "Please left-drag to select the tof range corresponding"\
            " to time-independent background" )
        figure = app.get_figure()
        axes = figure.gca()
        axes.plot( x,y )
        app.MainLoop()
        xlim = axes.get_xlim()
        #print xlim
        return xlim

    pass # end of TofWindowSelector
        


from  reduction.utils.plotting import wxmpl
class PlotApp(wxmpl.PlotApp):

    ABOUT_MESSAGE = "Left drag to zoom in.\n"\
                    "Right click to restore to the full range.\n\n"\
                    "When you exit this plot, the current x range "\
                    "will be chosen as\n"\
                    "the time-independent background range\n"\

    pass


# version
__id__ = "$Id$"

# End of file 
