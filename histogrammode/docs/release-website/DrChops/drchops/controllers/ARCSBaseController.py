from arcs.lib.base import *


class NavigatorItem:

    def __init__(self, name, active=False, link='/', accesskey=''):
        self.name = name
        self.active = active
        self.link = link
        self.accesskey = accesskey
        return

    def activate(self): self.active = True; return self

    def deactivate(self): self.active = False; return self

    pass # end of NavigatorItem


class Navigator:

    def __init__(self, items):
        self.items = items
        d = {}
        for item in items: d[item.name] = item
        self._name2item = d
        self.activeItem = items[0].activate()
        self.names = [ item.name for item in items ]
        return

    def activate(self, name):
        self.activeItem.deactivate()
        item = self._name2item[ name ]
        self.activeItem = item.activate()
        return

    pass # end of Navigator


class ARCSBaseController(BaseController):


    title = "Data Reduction for Chopper Spectrometers"
    long_title = "Data Reduction for Chopper Spectrometers"
    description = "Data Reduction for Chopper Spectrometers"
    latest_version = "1.2"
    nav_items = [
        NavigatorItem( "Home" ),
        NavigatorItem( "Docs", link = '/Docs'),
        #NavigatorItem( "Wiki", link = '/Wiki/Blank'),
        NavigatorItem( "Trac", link = '/Trac'),
        NavigatorItem( "FAQ", link = '/FAQ'),
        NavigatorItem( "Install", link = '/Install'),
        ]
    navigator = Navigator( nav_items )
    del nav_items


    def _create(self, menu, page_content):
        c.title = self.title
        c.description = self.description
        c.long_title = self.long_title
        c.latest_version = self.latest_version
        c.navigator = navigator = self.navigator
        
        navigator.activate( menu )
        
        c.page = page_content
        r = render_response( '/main.myt' )
        return r
        

    pass # end of MainController
