

import os
root = os.path.abspath(os.path.join( "drchops", "public"))


def path(url):
    return os.path.join( root, url )


def get_content( url ):
    f = path( url )
    return open( f ).read()

                           

## def get_content( project, url, encoding = 'utf-8' ):
##     """get content of html file that is drchops/parivate/proxy directory

##     project: the project to be proxied
##     url: url of the html file inside the project
##     """
##     f = os.path.join( path, project, url )
##     return codecs.open( f, 'r', encoding ).read()


## import codecs
