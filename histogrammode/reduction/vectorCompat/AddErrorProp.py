#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class AdditionErrorPropagator( object):

    def propagate( self, errVect1, errVect2, outputVect):
        from stdVector import add

        add( errVect1, errVect2, outputVect)

        return outputVect


    def __init__( self, *args, **kwds):
        return

    
# version
__id__ = "$Id: AddErrorProp.py 428 2005-05-18 14:42:04Z tim $"

# End of file
