import logging

from drchops.lib.base import *
from BaseController import BaseController

log = logging.getLogger(__name__)

class MainController(BaseController):

    def index(self, menuitem = None, url = None):
        if menuitem is None: menuitem = 'Home'
        if menuitem not in self.navigator.names:
            raise RuntimeError, "no such page: %r, %r" % (menuitem, url)
        if url is None: url = menuitem + '.html'
        environ = request.environ
        remote_host = environ.get('REMOTE_HOST')
        remote_addr = environ.get('REMOTE_ADDR')
        import time
        t = time.asctime()
        print "%s: request from %s, %s" % (t, remote_host, remote_addr)
        return self._create( menuitem, url )


    def _create_page(self, menuitem, url):
	if isinstance( menuitem, unicode ): menuitem = str(menuitem)

        text = get_body( get_content( url ) )
        text = unicode( text, 'utf-8' )
        c.doc = text
        
        default_template = "/NormalPage.mako"

        try:
            print 'render: menuitem=%s' % menuitem
            r =  render( '/%s.mako' % menuitem )
        except Exception, err:
            import traceback
            traceback.print_exc()
            print "_create_page: %s: %s" % (err.__class__.__name__, err)
            r =  render( default_template )

        r =  unicode( r, 'utf-8' )
        return r


    def _create(self, menuitem='Home', url=None):
        if url is None: url = "index.html"
        try:
            #try to create a "wrapper" of original page
            page_content = self._create_page( menuitem, url )
            return BaseController._create( self, menuitem, page_content )
        except Exception, err:
            import traceback
            traceback.print_exc()
            print "Error when serving %s/%s: %s, %s" % (
                menuitem, url, err.__class__.__name__, err )
            
            #if wrapping failed, serve the original file
            url = '/'+url
            if isinstance(url, unicode): url = str(url)
            return redirect_to( url )        
        
    pass # end of MainController


from drchops.model.main import get_content, path
import os


def get_body( htmltext ):
    startsig = '<body' 
    start = htmltext.find( startsig )
    if start == -1: return htmltext
    
    start = htmltext.find( '>', start ) + 1

    endsig =  '</body>' 
    end = htmltext.find( endsig )

    ret = htmltext[start: end]
    return ret
