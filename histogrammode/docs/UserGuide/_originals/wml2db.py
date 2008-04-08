#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import sys
sys.path.append( "/Users/linjiao/dv/web/ARCS" )

from arcs.wml.Parser import Parser
default_parser = Parser()


def parse( stream ): return default_parser.parse( stream )

def parse_file( filename ): return default_parser.parse( open( filename ) )



from arcs.wml.DocbookRenderer import Renderer as DocbookRenderer
default_docbookrenderer = DocbookRenderer()

def render_docbook(wiki):
    from arcs.wml.Options import Options
    options = Options('weaver')
    default_docbookrenderer.options = options
    return default_docbookrenderer.render( wiki )


import journal
#journal.debug('wml.elements').activate()
#journal.debug("docbook-renderer").activate()


def convert(infile, outfile):
    wiki = parse_file( infile )
    text = render_docbook( wiki )
    text = '\n'.join( text )
    open(outfile, 'w').write( text )
    return


def fixfigurespath(filename):
    cmd = 'cat %s | sed "s|/figures|figures|g" > .t && mv .t %s' % ( filename,  filename)
    print cmd
    import os
    os.system( cmd )
    return


def main():
    import sys
    argv = sys.argv
    infile = argv[1]
    outfile = argv[2]
    convert( infile, outfile )
    fixfigurespath( outfile )
    return

if __name__ == "__main__" : main()


# version
__id__ = "$Id: Paragraph.py,v 1.1.1.1 2005/03/08 16:13:43 aivazis Exp $"

# End of file 
