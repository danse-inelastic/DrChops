#!/usr/bin/env python

import wx, os



from MainFrame import MainFrame



class MainWindowApp(wx.PySimpleApp):


    def __init__(self, applications,  *args, **kwargs):
        self.applications = applications
        wx.PySimpleApp.__init__(self, *args, **kwargs)
        return
    

    def OnInit(self):
        self.frame = MainFrame(None, -1, "Reduction softwares",
                               applications = self.applications,)
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
##         self.frame = wx.Frame( None, -1, "hello" )
##         self.frame.Show(True)
        return True


# $Id: MainWindowApp.py,v 1.1 2006/08/09 23:09:22 linjiao Exp $
# end of file
