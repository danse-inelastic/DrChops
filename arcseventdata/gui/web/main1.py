#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import os


#The "request" object passed from simple http server
#request = {}
#print request
#convert it to a query string
query_string = '&'.join( '%s=%s' % (k, ','.join(v)) for k,v in request.iteritems() )
#print 'query_string: %s<br><br>' % query_string
os.environ['QUERY_STRING'] = query_string


#headers
#print 'headers: %s<br><br>' % headers
#os.environ[ 'CONTENT_TYPE' ] = headers['content-type']


#posted data
#posted = file_handle_for_posted_data.read()
#print posted


out = 'out.html'
err = 'err.html'
cmd = "./main.py >%s  2>%s" % (out, err)
if os.system( cmd ):
    print open( err ).read()
else:
    lines = open( out ).readlines()
    print '\n'.join( lines[1:] )
    

# version
__id__ = "$Id$"

# End of file 
