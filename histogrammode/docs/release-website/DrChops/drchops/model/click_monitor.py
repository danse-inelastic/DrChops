

import os
path = os.path.join( "drchops", "private", "click-monitor" )


def get_all_monitored_links():
    """return [link: redirect-link] dictionary
    """
    lines = open( os.path.join( path, 'monitored_links' ) ).readlines()
    rs = {}
    for i in range( len(lines)/2 ):
        link = lines[2*i].strip()
        redirect = lines[2*i+1].strip()
        assert redirect.startswith( '-->' ), \
               "wrong format of redirect link: %s" % redirect
        redirect = redirect[3:]
        rs[link] = redirect
        continue
    return rs


def register( link, time, source ):
    #should so some file locking here
    f = open( os.path.join( path, 'registry' ), 'a' )
    f.write( "%s, %s, %s\n" % (link, time, source) )
    f.flush()
    f.close()
    return

