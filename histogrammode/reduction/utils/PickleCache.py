
from DiskCache import DiskCache

from pickle import load, dump

class PickleCache(DiskCache):

    def _dump(self, stuff, path):
        f = open(path, 'w') 
        dump( stuff, f )
        f.close()
        return


    def _load(self, path):
        return load( open(path) )


    pass # end of PickleCache




def test():    
    
    class _(PickleCache):

        '''This cache can report number of entries in a directory
        '''

        def _hashableKey(self, key):
            return key.replace( '/', '-' )
        
        
        def _outdated(self, key):
            path = self._getPath( key )
            from os.path import getmtime
            return getmtime( path ) < getmtime( key )


        def _compute(self, key):
            import os
            return len(os.listdir(key) )

        pass #

    cache = _('test', '/tmp/testcache')

    import os, shutil
    from os.path import join
    tmpdir = '/tmp/testcache/d'
    if os.path.exists(tmpdir): shutil.rmtree( tmpdir )
    os.makedirs( join( tmpdir, '1' ) )
    
    assert cache.get( tmpdir ) == 1

    import time
    time.sleep(1.5)
    os.makedirs( join( tmpdir, '2' ) )
    assert cache.get( tmpdir ) == 2
    return


def main():
    test()
    return


if __name__ == '__main__': main()
