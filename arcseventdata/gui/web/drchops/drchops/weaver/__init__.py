#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def action_link(action, cgihome):
    from ActionLinkRenderer import ActionLinkRenderer
    renderer = ActionLinkRenderer( cgihome )
    return renderer.render( action )

def action_href(action, cgihome):
    from ActionHrefRenderer import ActionHrefRenderer
    renderer = ActionHrefRenderer( cgihome )
    return renderer.render( action )

def action_formfields( action, form ):
    from ActionMill_forForm import ActionMill_forForm
    renderer = ActionMill_forForm( form )
    return renderer.render( action )



def extend(weaver):
    from TableRenderer import TableRenderer
    from SlidableGalleryMill import SlidableGalleryMill
    from Plot_2DMill import Plot_2DMill
    Weavers = [
        TableRenderer,
        SlidableGalleryMill,
        Plot_2DMill,
        ]
    _extend_weaver( weaver, Weavers )
    return


def _extend_weaver( weaver, Weavers ):
    for i, W in enumerate(Weavers):
        exec 'Weaver%d = W' %i in locals()
        continue
    
    from opal.weaver.StructuralMill import StructuralMill
    code = []
    code.append( 'class _( %s, StructuralMill ):' % ','.join(
        [ 'Weaver%d' % i for i in range(len(Weavers)) ] ) )
    code.append( '  def __init__(self, *args, **kwds):' )
    code.append( '    StructuralMill.__init__(self, *args, **kwds)' )
    exec '\n'.join( code ) in locals()
    
    weaver.bodyMill.structuralMill = _(weaver.bodyMill.tagger)
    weaver.bodyMill.structuralMill.director = weaver.director
    return


# version
__id__ = "$Id$"

# End of file 
