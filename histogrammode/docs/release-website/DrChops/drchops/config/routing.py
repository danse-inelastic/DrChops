"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('error/:action/:id', controller='error')

    # CUSTOM ROUTES HERE

    #map.connect(':controller/:action/:id')
    map.connect('pyreapp/:appname/:todo/*url', controller='pyreapp', appname=None, todo=None, url='')
    map.connect('browser/:purpose/*url', controller='browser', purpose='readfile', url=None)
    map.connect('click_monitor/:id', controller='click_monitor')
    map.connect('lrmecs2ascii/:action', controller='lrmecs2ascii', action="form")
    map.connect(':menuitem/*url', controller='main', menuitem='Home', url=None)
    
    map.connect('*url', controller='template', action='view')

    return map
