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

## \package reduction.pyre.preprocessors.VPlateDataProcessor


import journal
debug = journal.debug('reduction.pyre.preprocessors.VPlateDataProcessor')


from VDataProcessor import VDataProcessor as base


class VPlateDataProcessor(base):
    

    class Inventory(base.Inventory):

        import pyre.inventory as pinv
        
        pass # end of Inventory


    def __init__(self, name= 'VPlateDataProcessor'):
        base.__init__(self, name )
        return



    def _update(self):
        engine = self._createEngine( )
        
        self._fineTuneDarkAngle()
        
        ei_main = self._getInput( 'ei_main' )
        mask = engine.getMask( ei_main )
        cc = engine.calibrationConstants( ei_main )

        self._setOutput( 'mask', mask )
        self._setOutput( 'calibration constants', cc )
        return
    

    def _fineTuneDarkAngle(self):
        vRun = self._getInput( 'vanadium' )
        ei_main = self._getInput( 'ei_main' )

        # I(det) for the given incident neutron energy
        Idet = self._engine.getIdet( ei_main )
        detaxes = Idet.axes()

        # scattering angle(det)
        from reduction.core.getDetectorInfo import getScatteringAngles
        instrument,g = vRun.getInstrument()
        phidet = getScatteringAngles(instrument, g, detaxes )
        assert phidet.unit() == degree

        #the estimated value of dark angle is provided when
        #user construct the vanadium plate sample assembly
        vanadiumPlate = vRun.getSampleAssembly()
        assert vanadiumPlate.name.lower().find('vanadium') != -1, \
               '''This is not a vanadium sample: %s''' % vanadiumPlate.name
        darkAngle = vanadiumPlate.darkAngle/degree
        
        #a small window for fitting
        a1 = darkAngle - 3.; a2 = darkAngle + 3.
        
        phis = phidet.data().storage().asNumarray()
        #find the first detector for which phi is in the window
        #!!! this supposes that phi is ascending
        for i,phi in enumerate(phis):
            if phi>a1: i1 = i; break
            continue
        for i,phi in enumerate(phis):
            if phi>a2: i2 = i; break
            continue

        try: i1, i2
        except:
            raise RuntimeError , "Cannot find out the range of detectors that are around dark angle. This dark angle finder assumes that scattering angles of detectors ascends with detector ID."

        # a slice enclosing the darkAngle region
        x = phis[ i1: i2 ]
        
        Is = Idet.data().storage().asNumarray()
        y = Is[i1:i2]
        debug.log('phi, I= %s, %s' % (x, y ) )

        # fit I(phi) aroudn dark angle region to a parabolic function
        from reduction.vectorCompat.PolynomialFitter import PolynomialFitter
        a = PolynomialFitter(2).fit( x,y )

        #the dark angle computed:
        darkAngle = -a[1]/2./a[2] * phidet.unit()
        debug.log( "darkAngle=%s" % darkAngle )

        #set the dark angle of the sample assembly
        vanadiumPlate.setDarkAngle( darkAngle )
        return
    

    pass # end of VPlateDataProcessor


import reduction.units as units
degree = units.angle.degree


# version
__id__ = "$Id: VPlateDataProcessor.py 1270 2007-06-20 01:15:57Z linjiao $"

# End of file 
