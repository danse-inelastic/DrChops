
from AbstractCache import AbstractCache as base

class DiskCache(base):


    def __init__(self, name, path):
        base.__init__(self, name)
        self._path = path
        import os
        if not os.path.exists( path ): os.makedirs( path )
        if not os.path.isdir( path ):
            raise IOError, "%s is not a directory" % (path, )
        return


    def _cached( self, key ):
        import os
        return os.path.exists( self._path )


    def _hashableKey( self, key ):
        raise NotImplementedError


    def _makeCache(self, key, value):
        self._dump( value, self._getPath(key) )
        return
    

    def _getPath(self, key):
        hkey = self._hashableKey( key )
        from os.path import join
        return  join(self._path, self._hashableKey(key) )


    def _dump(self, stuff, path ):
        raise NotImplementedError


    def _get(self, key):
        path = self._getPath( key )
        try:
            return self._load( path )
        except Exception, err:
            raise
            raise ValueError


    def _load(self, path):
        raise NotImplementedError


    def _cached(self, key):
        path = self._getPath( key )
        import os
        return os.path.exists( path )


    pass # end of DiskCache


