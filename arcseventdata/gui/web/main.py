#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao  Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import sys

webapp_path = 'drchops'

paths_to_prepened = [
    webapp_path,
    ]

paths_to_prepened.reverse()
for path in paths_to_prepened:
    if path not in sys.path: sys.path = [path] + sys.path
    continue

#print 'sys.path=%s<br><br>' % sys.path



def main():
    import journal
    journal.error('pyre.inventory').deactivate()
    
    from drchops.applications.WebApplication import WebApplication


    class MainApp(WebApplication):


        def __init__(self):
            WebApplication.__init__(self, name='main')#, asCGI=True)
            return


        def run(self):
            WebApplication.run(self)
            return


    app = MainApp()
    return app.run()


if __name__== '__main__': main()

# version
__id__ = "$Id$"

# End of file 
