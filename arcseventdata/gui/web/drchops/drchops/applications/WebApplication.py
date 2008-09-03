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


from opal.applications.WebApplication import WebApplication as Base


class WebApplication(Base):

    class Inventory(Base.Inventory):

        # properties
        db = pyre.inventory.str(name='db', default='drchops')
        db.meta['tip'] = 'The name of the data base'

        dbwrapper =  pyre.inventory.str(name='dbwrapper', default='psycopg')
        dbwrapper.meta['tip'] = "the python package that provides access to the database back end"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import pyre.inventory
        import drchops.components
        clerk = pyre.inventory.facility( 'clerk', factory = drchops.components.clerk )


    def _configure(self):
        super(Base, self)._configure()
        self.clerk = self.inventory.clerk
        self.idd = self.inventory.idd
        
        self.pageMill.director = self

        from drchops.weaver import extend
        extend(self.pageMill)
        return
        

    def _init(self):
        super(Base, self)._init()

        # connect to the database
        import pyre.db
        self.db = pyre.db.connect(
            database=self.inventory.db, wrapper=self.inventory.dbwrapper)
        
        # initialize the accessors
        self.clerk.db = self.db
        return
        

    def _getPrivateDepositoryLocations(self):
        return ['drchops/content', 'drchops/config']


# version
__id__ = "$Id: WebApplication.py,v 1.1.1.1 2006-11-27 00:09:19 aivazis Exp $"

# End of file 
