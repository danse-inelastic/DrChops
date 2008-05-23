#!/usr/bin/env python
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


def FunctorFromFunction( func ):
    '''convenient function to create a functor class from a function,
    so that it can be used with FacilityFrontEnd'''
    
    class Klass:

        __doc__ = "Functor of function: %s" % func.__doc__

        def __init__(self):
            '__init__()'
            return

        def __call__(self, *args, **kwds):
            return func(*args, **kwds)

        __call__.__doc__ = func.__doc__


        def __getattr__(self, key):
            return getattr( func, key )

        pass # end of Klass
    
    return Klass
            


# version
__id__ = "$Id$"

# End of file 
