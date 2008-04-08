#!/usr/bin/env python
# T. M. Kelley tkelley@caltech.edu (c) 2004

## \package reduction.vectorCompat.TemplateCObject
## Provides base class that minds a handle, classname, and a template type
## for classes that wrap C++ template objects
##
## This is for connection python objects to c++ template class objects


from CObject import CObject

class TemplateCObject( CObject):
    """Base class that minds a handle, classname, and a template type
    for classes that wrap C++ template objects
    """

    def templateType( self):
        """Get the name of the template class for this object.
        """
        return self._templateType

    datatype = templateType


    def __init__( self, templateType = None, handle = None, klass = None,
                  classID = 0):
        """TemplateCObject( templateType, handle, className) 
        """
        CObject.__init__( self, handle, klass, classID)
        self._templateType = templateType
        return


    def _isCompatible( self, other):
        if self.templateType() != other.templateType():
            msg = "template (data) types do not agree, this obj's type ="
            msg += str( self.templateType()) + ", other's type = "
            msg += str( other.templateType())
            raise TypeError, msg
        return CObject._isCompatible( self, other)

# version
__id__ = "$Id: TemplateCObject.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
