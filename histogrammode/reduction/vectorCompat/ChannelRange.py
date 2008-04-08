#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved

class ChannelRange( object):
    """Convenient way to specify a range [start, end).
    end is one-past-the last one in the range"""

    def end( self):
        """One past the end of the range"""
        return self._end


    def numChannels( self):
        return (self._end - self._start)


    def start( self):
        return self._start


    def __init__( self, start, end):
        self._start = start
        self._end = end
        return
        

# version
__id__ = "$Id: ChannelRange.py 381 2005-04-14 17:13:59Z tim $"

# End of file
