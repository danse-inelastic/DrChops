#!/usr/bin/env python

import wx, wx.lib.dialogs
import os


class MainFrame(wx.Frame):
    
    
    try:
        # in case this is installed by distutils_adpt
        # we should have a install_info.py.
        # we can query that file to know where files are installed
        from install_info  import share
        iconpath = os.path.join( share, "reduction", "resources","icons")
    except:
        # in case this is installed by Michael Aivazis build procedure
        iconpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "..", "..", '..', '..',
                                'share', 'reduction', "resources","icons" )

    
    def __init__(self, parent=None, id=-1, name = "reduction softwares",
                 pos = wx.DefaultPosition,
                 applications = [] ):
        self.threads = []
        self.applications = applications
        for app in self.applications:
            buttonfile = "%s.png" % app['name']
            buttonfile = os.path.join( self.iconpath, buttonfile )
            print buttonfile
            image = wx.Image(buttonfile, wx.BITMAP_TYPE_PNG)
            bmp = image.ConvertToBitmap()
            app['bmp'] = bmp
            continue
            
        #size = self.img.GetWidth(), self.img.GetHeight()
        wx.Frame.__init__(self, parent, id, name, pos, (100,200))
        print "MainFrame %s created" % name
        self.drawscreen()
        return


    def drawscreen(self):

        vSizer = wx.BoxSizer( wx.VERTICAL )

        title = wx.StaticText( self, -1, "Reduction applications")
        title.SetFont( wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD ) )
        vSizer.Add( title, 0, wx.ALIGN_CENTER)

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )

        for app in self.applications:
            bmp = app['bmp']
            button = wx.BitmapButton(self, -1, bmp, pos = (200, 150))
            appName = app['name']
            button.SetToolTipString('run %s' % appName )
            exe = app['exe']
            self.Bind(wx.EVT_BUTTON, self.OnRunApp(exe) , button)
            buttonSizer.Add( button, 1, wx.GROW | wx.ALL, 15 )
            continue

        vSizer.Add( buttonSizer, 0, wx.ALIGN_CENTER)
        
        border = wx.BoxSizer()

        border.Add(vSizer, 1, wx.GROW|wx.ALL, 25)
        border.Fit(self)
        self.SetSizer(border)
        self.Layout()
        return


    def OnRunApp(self, exe):
        def _(evt):
            thread = PyreAppThread(exe)
            self.threads.append( thread )
            thread.start()
            return
        return _


    def OnExitButton(self, evt):
        self.Close()
        return

    # end of MainFrame


from threading import Thread
class PyreAppThread( Thread ):

    def __init__(self, pyreexecutable):
        Thread.__init__(self)
        self.pyreexe = pyreexecutable
        return


    def run(self):
        from pyregui.launchers.spawn import spawn
        from pyregui.utils import findExecutable
        pexe = findExecutable( self.pyreexe )
        spawn( pexe )
        return

        
    

# end of file
