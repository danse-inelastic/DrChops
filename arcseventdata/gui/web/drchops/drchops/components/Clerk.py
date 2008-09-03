# -*- Python -*-
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


from pyre.components.Component import Component as base


class Clerk( base ):

    class Inventory( base.Inventory):

        import pyre.inventory
        db = pyre.inventory.str('db', default = 'db-pickles' )
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        base.__init__(self, name, facility)
        return


    def newRecord(self, record):
        tablename = record.__class__.__name__
        store = self._retrieve_store( tablename )
        store[ record.id ] = record
        self._update_store( tablename, store )
        return


    def updateRecord(self, record):
        tablename = record.__class__.__name__
        store = self._retrieve_store( tablename )
        store[ record.id ] = record
        self._update_store( tablename, store )
        return


    def getRecordByID(self, table, id):
        store = self._retrieve_store( table )
        return store[ id ]


    def _retrieve_store(self, tablename):
        if tablename in self._cache : return self._cache[ tablename ]
        else:
            path = self._store_path( tablename )
            if not os.path.exists( path ): ret = dict()
            else:
                f = open(path) 
                ret = pickle.load( f )
                f.close()
                
            self._cache[ tablename ] = ret
            
            return ret


    def _update_store(self, tablename, newstore):
        store = self._retrieve_store( tablename )
        store.update( newstore )
        return


    def _store_path(self, tablename):
        return os.path.join( self.db, tablename )
    

    def _configure(self):
        base._configure(self)
        self.db = self.inventory.db
        return


    def _init(self):
        base._init(self)
        self._cache  = {}
        return


    def _fini(self):
        for name, store in self._cache.iteritems():
            path = self._store_path( name )
            pickle.dump( store, open( path, 'w') )
        base._fini(self)
        return
    

import os
import pickle


# version
__id__ = "$Id$"

# End of file 
