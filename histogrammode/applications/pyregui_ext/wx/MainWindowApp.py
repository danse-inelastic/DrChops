#!/usr/bin/env python



from pyregui.guitoolkit.wx.MainWindowApp import MainWindowApp as Base


import os


class MainWindowApp(Base):


    def _buttonfile(self):
        try:
            # in case this is installed by distutils_adpt
            # we should have a install_info.py.
            # we can query that file to know where files are installed
            from install_info  import share
            buttonfile = os.path.join( 
                share, "reduction", "resources","icons",'ARCS.png')
        except:
            # in case this is installed by Michael Aivazis build procedure
            buttonfile = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..', "..","..","..","..",
                "share",'reduction', 'resources', "icons",'ARCS.png')
        return buttonfile
    

    pass # end of MainWindowApp



# $Id: MainWindowApp.py,v 1.2 2006/08/05 06:49:28 patrickh Exp $
# end of file
