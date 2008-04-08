#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

## \package reduction.histCompat.VSampleParams
## vanadium sample parameters
##


class VSampleParams( object):

    """ Class to gather information of a vanadium plate sample"""

    def darkAngle( self):
        """darkAngle() -> dark angle with unit attached
        The angle of the long axis of the plate in the spectrometer in
        degrees, which is also the angle of least transmission for a V
        plate."""
        return self._darkAngle


    def thickness( self):
        """thickness of plate. unit attached"""
        return self._thickness


    def width( self):
        """width of plate. unit attached"""
        return self._width


    def __init__( self, darkAngle, thickness, width):
        """VSampleProperties( darkAngle, thickness, width) -> VSampleProps
        Create a new VSampleProperties instance.
        All inputs must have units attached.
        Inputs:
            darkAngle: angle of long horiz axis of plate in spect.
            thickness: of plate 
            width: of plate 
        Output:
            new VSampleProperties instance
        Exceptions: None
        Notes: None"""
        self._darkAngle = darkAngle
        self._thickness = thickness
        self._width = width
        return

    
# version
__id__ = "$Id: VSampleParams.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
