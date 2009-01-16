#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from reduction.pyre.datasource.LrmecsMeasurement import LrmecsMeasurement
from reduction.pyre.SqeReducer import SpeReducer
from reduction.pyre.Spe2Sqe import Spe2Sqe
from pyregui.inventory.extensions.OutputDir import OutputDir

from reduction.pyre.Composite import Composite as base

from reduction.pyre.inventory.Inventory import ObserveTrait

class PowderReduction(base):


    '''Reduce powder data to S(Q,E)

    This reducer obtains measured histograms from data sources,
    reduces the I(det, pix, tof) histogram to a S(Q,E) histogram.
    Calibrations and corections are performed in this reduction
    procedure if corresponding data are available.
    '''

    class Inventory( ObserveTrait, base.Inventory ):
        import pyre.inventory as inv

        measurementFactory = inv.facility(
            'measurementFactory', default = LrmecsMeasurement())
        measurementFactory.meta['importance'] = 1000
        measurementFactory.meta['tip'] = "Measurement"

        SpeReducer = inv.facility( 'SpeReducer', factory = SpeReducer )
        SpeReducer.meta['tip'] = 'Reduce data to S(phi,E)'
        SpeReducer.meta['importance'] = 800
        
        Spe2Sqe = inv.facility( 'Spe2Sqe', factory = Spe2Sqe )
        Spe2Sqe.meta['tip'] = 'S(phi,E) --> S(Q,E)'
        Spe2Sqe.meta['importance'] = 600

        outputDir = OutputDir( 'outputDir', default = "." )
        outputDir.meta['tip'] = 'Output directory'

        gui = inv.bool( 'gui', default = False )
        gui.meta['opacity'] = 100

        pass #


    connections = [
        'measurementFactory:measurement->measurement:SpeReducer',
        'SpeReducer:Ei->Ei:Spe2Sqe',
        'SpeReducer:spe->spe:Spe2Sqe',
        'Spe2Sqe:sqe->sqe:self',
        'SpeReducer:Ei->Ei:self',
        ]

    
    sockets = {
        'in': [],
        'out': ['sqe'],
        }


    def __init__(self, name = 'PowderReduction'):
        base.__init__( self, name )
        SpeReducer = self.inventory.SpeReducer
        self._measurementObserver = MeasurementObserver(self)

        self.inventory.registerTraitObserver( 'measurementFactory', self )
        self.update( self.inventory.measurementFactory )
        return


    def update(self, value):
        mi = self.inventory.measurementFactory.inventory
        mi.registerObserver(self._measurementObserver )
        return


    def _defaults(self):
        base._defaults(self)
        return
    

    def _configure(self):
        base._configure(self)
        if self._showHelpOnly: return

        mi = self.inventory.measurementFactory.inventory
        self._measurementObserver.update( mi )

        if self.inventory.gui:
            preprocess = self.inventory.SpeReducer.inventory.preprocess
            preprocess.inventory.preStep1 = 'preStep1_withTibgWindowPicker'
            preprocess.inventory.preStep1_main = 'preStep1_withTibgWindowPicker'
            preprocess.inventory.preStep1_mt = 'preStep1_withTibgWindowPicker'
            preprocess.inventory.configureComponents()
            pass
            
        return


    def _init(self):
        base._init(self)
        outputDir = self.inventory.outputDir
        import os
        os.chdir( outputDir )
        return

    pass #



from Preprocess_All import Preprocess_All
from Preprocess_MainDataOnly import Preprocess_MainDataOnly
from Preprocess_Main_and_MT import Preprocess_Main_and_MT
from Preprocess_Main_and_Calib import Preprocess_Main_and_Calib


class MeasurementObserver:

    import journal
    debug = journal.debug( 'MeasurementObserver' )
    del journal

    def __init__(self, managed):
        self.managed = managed
        return

    def update(self, inventory):
        self.debug.log( "update called" )
        
        reducer = self.managed
        
        SpeReducer = reducer.inventory.SpeReducer
        
        if inventory.main != '' and inventory.mt != '' and inventory.calib != '':
            SpeReducer.inventory.preprocess = Preprocess_All()
        elif inventory.main != '' and inventory.mt == '' and inventory.calib != '':
            SpeReducer.inventory.preprocess = Preprocess_Main_and_Calib()
        elif inventory.main != '' and inventory.mt != '' and inventory.calib == '':
            SpeReducer.inventory.preprocess = Preprocess_Main_and_MT()
        elif inventory.main != '' and inventory.mt == '' and inventory.calib == '':
            SpeReducer.inventory.preprocess = Preprocess_MainDataOnly()
        else:
            pass

        # this is a hack to add alias to the component. should probably use a string
        # to load the component so that alias is attached automatically
        SpeReducer.inventory.preprocess.aliases.append(SpeReducer.Inventory.preprocess.name)
        
        SpeReducer.inventory.configureComponents()
        return

    pass# end of MeasurementObserver

# implementatino notes:
## This component is implmented using inventory observer. We must be very careful
## about how we use those observers. If two observers are setting attributes of
## one component according to different inputs, confusions could come up.
## Be very careful...
    

# version
__id__ = "$Id$"

# End of file 
