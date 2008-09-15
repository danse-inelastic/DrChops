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

        pass
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        super(Clerk, self).__init__(name=name, facility=facility)
        return


    def newJob(self):
        from drchops.dom.Job import Job
        return self._newRecord( Job )


    def newVanadiumReduction(self):
        from drchops.dom.VanadiumReduction import VanadiumReduction
        return self._newRecord( VanadiumReduction )


    def newReductionToMslice(self):
        from drchops.dom.ReductionToMslice import ReductionToMslice
        return self._newRecord( ReductionToMslice )


    def newReduction(self):
        director = self.director
        
        # create a new reduction
        from drchops.dom.Reduction import Reduction
        reduction = Reduction()
        reduction.id = new_id(director)
        
        # create a new measurement
        from drchops.dom.Measurement import Measurement
        measurement = Measurement()
        measurement.id = new_id(director)
        
        #
        reduction.measurement = measurement

        self.db.insertRow( measurement )
        self.db.insertRow( reduction )
        
        return reduction


    def getJob(self, id):
        return self.getRecordByID( 'Job', id )


    def getVanadiumReduction(self, id):
        return self.getRecordByID( 'VanadiumReduction', id )


    def getFinishedVanadiumReductions(self):
        from drchops.dom.VanadiumReduction import VanadiumReduction as table
        all = self.db.fetchall( table )
        from ReductionResultsRetriever import retrieve
        return filter( lambda r: retrieve(r, self.director), all )


    def getReductionToMslice(self, id):
        return self.getRecordByID( 'ReductionToMslice', id )


    def getRecordByID(self, tablename, id):
        exec 'from drchops.dom.%s import %s as Table' % (tablename, tablename) \
             in locals()
        return self._getRecordByID( Table, id )


    def updateRecord(self, record):
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        for column in record.getColumnNames():
            value = getattr( record, column )
            #value = _tostr( value )
            assignments.append( (column, value) )
            continue
        
        self.db.updateRow(record.__class__, assignments, where)
        return record


    def insertRecord(self, record):
        self.db.insertRow( record )
        return record


    def _newRecord(self, table):
        r = table()
        id = new_id(self.director)
        r.id = id
        db = self.db
        db.insertRow(r)
        return r

    
    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)
    
    

import os
import pickle
from misc import empty_id, new_id


# version
__id__ = "$Id$"

# End of file 
