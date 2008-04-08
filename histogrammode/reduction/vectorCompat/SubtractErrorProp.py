#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class SubtractErrorPropagator( object):

    def propagate( self, errVect1, errVect2, outputVect):
        from stdVector import add

        add( errVect1, errVect2, outputVect)

        return outputVect


    def __init__( self, *args, **kwds):
        return

    
# version
__id__ = "$Id: SubtractErrorProp.py 436 2005-05-18 16:46:26Z tim $"

# End of file
