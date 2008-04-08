
class AbstractCache:

    def __init__(self, name):
        self.name = name
        return


    def get(self, key):
        if not self._cached( key ) or self._outdated( key ):
            return self._initCache(key)
        try:
            return self._get( key )
        except ValueError, err:
            #this means the cache is broken
            #try to force initialization
            return self._initCache( key )

        raise "Should not reach here"


    def _initCache( self, key ):
        ret = self._compute( key )
        self._makeCache( key, ret )
        return ret


    def _cached( self, key ):
        raise NotImplementedError


    def _outdated(self, key):
        raise NotImplementedError


    def _compute(self, key ):
        raise NotImplementedError


    def _makeCache(self, key, value):
        raise NotImplementedError


    def _get(self, key):
        raise NotImplementedError
    
    pass




