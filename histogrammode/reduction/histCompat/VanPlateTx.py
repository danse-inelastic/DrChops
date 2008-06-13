#!/usr/bin/env python
# T. M. Kelley tkelley@caltech.edu (c) 2003

## \package reduction.histCompat.VanPlateTx
## calculate transmission coefficients through the vanadium sample
##
## This implementation directly calls python bindings of libreduction


from reduction import reduction as red

import journal
debug = journal.debug('VanPlateTx')


from pyre.units.length import cm
from pyre.units.angle import degree, radian
from pyre.units.energy import meV

class VanPlateTx(object):
    
    """calculator to compute transmission through a thin vanadium plate.
    """
    
    def __init__(self, vSampleParams):
        """
        ctor: VanPlateXmission( darkAngle, thickness, width)
        Create a functor to compute the transmission through a thin Vanadium plate.
        All inputs must have physical units attached, for example
        
            VanPlateTx( Vsampleparams( 135*degree, 0.2*cm, 7*cm )
            
        inputs:
            darkAngle (angle from tranmitted beam to long axis of plate, viewed
                       from above)
            thickness (of plate)
            width (of plate, (dimension parallel to dark-angle axis);)
        outputs:
            PyCObject/void ptr to new object
        Exceptions: ValueError
        """
        
        darkAngle = vSampleParams.darkAngle()/degree
        thickness = vSampleParams.thickness()/cm
        width = vSampleParams.width()/cm
        
        #print "darkAngle: %s, thickness: %s, width %s" % (darkAngle, thickness, width)
        debug.log( "darkAngle: %s, thickness: %s, width %s" % (darkAngle, thickness, width) )
        self._handle = red.vanPlateXmission_ctor( darkAngle, thickness, width)

        return


    def __call__(self, detectorAngle, energy):
        """instance(  detectorAngle, energy)
        All inputs must have physical units attached
        inputs:
            detectorAngle 
            energy
        outputs:
            transmission coefficient (float)
        Exceptions: ValueError
        """
        detectorAngle = detectorAngle/radian
        energy = energy / meV
        return red.vanPlateXmission_call( self._handle, detectorAngle, energy)


    def calc_tx_phi(self, energy, angleaxis):
        '''calculate a Tx(phi) histogram

        angleaxis: phi axis
        energy: neutron energy. must have unit attached
        '''
        assert angleaxis.name() == 'phi'
        from histogram import histogram
        res = histogram( 'V plate tx(phi)', [angleaxis])
        for phi in res.phi:
            res[ phi ] = self( phi*degree, energy ), 0
            continue
        return res

    

# version
__id__ = "$Id: VanPlateTx.py 1431 2007-11-03 20:36:41Z linjiao $"

# End of file
