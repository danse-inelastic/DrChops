import logging

from drchops.lib.base import *

import os
root = os.path.abspath( '.' )
pub_tmp = os.path.join( root, 'drchops', 'public', 'tmp' )
if not os.path.exists(pub_tmp) : os.makedirs( pub_tmp )
elif not os.path.isdir(pub_tmp): raise "% is not a directory" % pub_tmp


log = logging.getLogger(__name__)

from BaseController import BaseController
class Lrmecs2AsciiController(BaseController):

    def form(self):
        return self._create(
            menuitem = 'Docs',
            page_content = render( "/lrmecs2ascii/form.mako" ) )

            
    def upload(self):
        #store uploaded file to a tmp file
        uploaded_file = request.POST['uploaded_file']
        if uploaded_file == '': h.redirect_to(action='form')
        filename = uploaded_file.filename
        import os
        tmp = '/tmp'
        save_filename = os.path.join(tmp, filename)
        save_file = open(save_filename, 'w')
        import shutil
        shutil.copyfileobj(uploaded_file.file, save_file)
        uploaded_file.file.close()
        save_file.close()

        session['uploaded_file'] = save_filename
        session.save()
        #redirect
        h.redirect_to(action='convert')
        return


    def convert(self):
        uploaded_file = session['uploaded_file']
        filename = os.path.split(uploaded_file)[-1]
        newfilename = os.path.splitext(filename)[0] + '.txt'
        converted = os.path.join( pub_tmp, newfilename )
        cmd = "lrmecs2ascii %s > %s" % (uploaded_file, converted)
        print cmd
        if os.system( cmd ): h.redirect_to(action='failed'); return
        session['download_link'] = '/tmp/' + newfilename
        session.save()
        h.redirect_to(action="result")
        return


    def failed(self):
        return Response('Unable to perform lrmecs binary data file --> ascii file conversion')
        

    def result(self):
        download_link = session['download_link']
        c.download_link = download_link
        return self._create(
            menuitem = 'Docs',
            page_content = render( "/lrmecs2ascii/result.mako" ) )

        
