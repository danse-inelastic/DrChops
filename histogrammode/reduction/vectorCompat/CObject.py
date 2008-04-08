#!/usr/bin/env python
# T. M. Kelley tkelley@caltech.edu (c) 2004


## \package reduction.vectorCompat.CObject
## Provides the mix-in class that provides handle and type methods.
##
## This facilitates connection of python objects to underlying c++ objects


class CObject( object):
    """Mix-in class that provides handle and type methods
    """

    def handle( self):
        """Get the PyCObject with a void pointer to type
        """
        return self._handle


    def name( self):
        """Get the name of the class/type this CObject wraps
        """
        return self._type


    def classID( self):
        return self._classID

    def __init__( self, handle = None, klass = None, classID = 0):
        self._handle = handle
        self._type = klass
        self._classID = classID
        return


    def _isCompatible( self, other):
        if self.name() != other.name():
            msg = "C++ class types do not agree, this object's class name ="
            msg += str( self.name()) + ", other's class name = "
            msg += str( other.name())
            raise TypeError, msg
        if self.classID() != other.classID():
            msg = "Class IDs do not agree, this object's ID ="
            msg += str( self.classID()) + ", other's ID = "
            msg += str( other.classID())
            raise TypeError, msg
        return

    
# version
__id__ = "$Id: CObject.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
