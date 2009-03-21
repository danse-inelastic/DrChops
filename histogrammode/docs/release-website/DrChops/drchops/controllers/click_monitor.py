from drchops.model.click_monitor import register as _register, get_all_monitored_links


class ClickMonitor(object):

    def __init__(self):
        self.links = get_all_monitored_links ()
        return
    
    
    def monitored(self, link):
        return link in self.links.keys()
    
    
    def register( self, link, time, source ):
        _register( link, time, source )
        return


    def get_redirect( self, link ): return self.links[link]


    pass # end of Click_monitor

    

import logging

from drchops.lib.base import *

log = logging.getLogger(__name__)

class ClickMonitorController(BaseController):
    
    def __init__(self, *args, **kwds):
        BaseController.__init__(self, *args, **kwds)
        self._engine = ClickMonitor( )
        return

    
    def index(self, id):
        engine = self._engine
        if not engine.monitored( id ):
            return '%s is not monitored' % id
            return Response('%s is not monitored' % id)
        
        import time
        t = time.ctime()
        
        environ = request.environ
        src = environ.get('REMOTE_HOST')
    
        if src: engine.register( id, t, src )
        return redirect_to( engine.get_redirect( id ) )
    
    pass # end of ClickMonitorController
