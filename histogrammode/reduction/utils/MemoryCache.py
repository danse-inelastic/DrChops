
from AbstractCache import AbstractCache as base

class MemoryCache( base ):

    def __init__(self, *args, **kwds ):
        base.__init__(self, *args, **kwds)
        self._memo = {}
        return

    
    def set(self, key, value):
        hkey = self._hashableKey( key )
        self._memo[hkey] = value
        return
    

    def _cached( self, key ):
        hkey = self._hashableKey(key)
        return self._memo.has_key( hkey )


    def _hashableKey(self, key):
        raise NotImplementedError


    def _outdated(self, key):
        return False


    def _makeCache(self, key, value):
        hkey = self._hashableKey( key )
        self._memo[hkey] = value
        return


    def _get(self, key):
        hkey = self._hashableKey( key )
        return self._memo[hkey]
    
    

def test():    
    
    class _(MemoryCache):

        '''This cache is simply a dictionary
        '''

        def _hashableKey(self, key):
            return key
        
        pass #

    cache = _('test')

    cache.set( 'a' , 1 )
    assert cache.get('a') == 1
    return


def main():
    test()
    return


if __name__ == '__main__': main()
