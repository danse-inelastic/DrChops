#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
debug = journal.debug('db' )


from pyre.db.DBManager import DBManager as base
class DBManager(base):


    def __init__(self, name):
        self.name = name

        import pyre.parsing.locators
        self.locator = pyre.parsing.locators.simple("%s database" % name)

        self._cache = {}
        return


    def autocommit(self, flag=True):
        self._autocommit = flag
        return


    def commit(self):
        for name, store in self._cache.iteritems():
            path = self._store_path( name )
            pickle.dump( store, open( path, 'w') )
        return


    def connect(self, **kwds):
        return


    def cursor(self):
        raise NotImplementedError


    def insertRow(self, row, tableName=None):
        if tableName is None:
            tableName = row.__class__.__name__
        store = self._retrieve_store( tableName )
        store[ row.id ] = row
        self._update_store( tableName, store )
        return


    def updateRow(self, table, assignments, where=None):
        row = table()
        for col, value in assignments:
            row._setColumnValue( col, value )
            continue
        
        tablename = table.__name__
        store = self._retrieve_store( tablename )
        store[ row.id ] = row
        self._update_store( tablename, store )
        return


    def deleteRow(self, table, where=None):
        sql = "DELETE FROM %s" % table.name
        if where:
            sql += "\n    WHERE %s" % where

            # execute the sql statement
            c = self.db.cursor()
            c.execute(sql)
            self.db.commit()

            return


    def createTable(self, table):
        # build the list of table columns
        fields = []
        for name, column in table._columnRegistry.iteritems():
            text = "    %s %s" % (name, column.declaration())
            fields.append(text)

        # build the query
        sql = "CREATE TABLE %s (\n%s\n    )" % (table.name, ",\n".join(fields))

        # execute the sql statement
        c = self.db.cursor()

        try:
            c.execute(sql)
        except:
            debug.log( 'sql: %s' % sql )
            raise
        self.db.commit()

        return


    def dropTable(self, table, cascade=False):
        sql = "DROP TABLE %s" % table.name
        if cascade:
            sql += " CASCADE"

        # execute the sql statement
        c = self.db.cursor()
        c.execute(sql)

        return


    def fetchall(self, table, where=None, sort=None):
        columns = table._columnRegistry.keys()
        
        # build the sql statement
        sql = "SELECT %s FROM %s" % (", ".join(columns), table.name)
        if where:
            sql += " WHERE %s" % where
        if sort:
            sql += " ORDER BY %s" % sort
        
        # execute the sql statement
        c = self.db.cursor()
        try:
            c.execute(sql)
        except:
            debug.log( 'sql: %s' % sql )
            raise
        #print c.fetchall(),'<br>'
        #print c.fetchall(),'<br>'
        # walk through the result of the query
        items = []
        for row in c.fetchall():
            # create the object
            item = table()
            item.locator = self.locator
            
            # build the dictionary with the column information
            values = {}
            for key, value in zip(columns, row):
	    	if value is not None:
                    values[key] = value
            # attach it to the object
            item._priv_columns = values

            # add this object tothepile
            items.append(item)

        return items


    def _find(self, tablename, where):
        expr = where.replace( '=', '==' ) # 

        store = self._retrieve_store( tablename )
        for k, v in store.iteritems():
            
        return


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
        return os.path.join( self.name, tablename )
    


import pickle


# version
__id__ = "$Id: DBManager.py,v 1.4 2008-04-21 03:07:30 aivazis Exp $"

# End of file 
