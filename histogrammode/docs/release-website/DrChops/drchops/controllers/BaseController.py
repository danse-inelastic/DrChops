from drchops.lib.base import *
from MainMenu import mainmenu


from drchops.lib.base import BaseController as base
class BaseController(base):

    title = "Data Reduction for Chopper Spectrometers"
    long_title = "Data Reduction for Chopper Spectrometers"
    description = "Data Reduction for Chopper Spectrometers"
    latest_version = "1.3pre1"
    navigator = mainmenu

    def _create(self, menuitem, page_content):
        c.title = self.title
        c.description = self.description
        c.long_title = self.long_title
        c.latest_version = self.latest_version
        c.navigator = self.navigator
        
        self.navigator.activate( menuitem )
        
        c.page = page_content
        r = render( '/main.mako' )
        return r
        

    pass # end of BaseController
