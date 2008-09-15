# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from opal.components.Actor import Actor as base
from drchops.content import action
from drchops.weaver import action_link


class Actor(base):

    def redirect(self, director, actor, routine, *args, **kwds):
        actor = director.retrieveActor( actor )
        director.routine = routine
        director.configureComponent( actor )
        director.actor = actor
        return getattr(actor, routine)( director, *args, **kwds )
        
# version
__id__ = "$Id$"

# End of file 
