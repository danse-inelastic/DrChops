#!/usr/bin/env python
# Timothy M. Kelley Copyright (c) 2005 All rights reserved


## \package reduction.vectorCompat.He3DetEffic
## Calculate efficiency of He3 detector tube
## 



from reduction import reduction as red

from TemplateCObject import TemplateCObject as Base


import journal
debug  =  journal.debug("He3DetEffic")


##   Functor to compute He3 detector tube efficiency given neutron energy.
## 
##   Detector tube is assumed to be a cylinder.
##   Pressure in the tube is assumed to be steady and uniform.
##
##   This python class is a wrapper of c++ class reduction.He3DetEffic.
##   Its algorithm is a straighforward integration. Neutron could pass
##   a detector tube at various paths, but this problem becomes a simple one
##   with an assumption: all neutrons run through the tube in perpendicular
##   to the axis of the tube.
##   Therefore, the only integration variable is the distance from
##   tube center axis to the neutron trace.
##
##   Constructor takes detector radius, pressure, and number of points
##   for integration as inputs.
##
##   Usage:
##     >>> effCalculator = He3DetEffic( pressure, radius ) # pressure units: atmossphere, radius units: cm
##     >>> eff = effCalculator(energy) # energy units: meV. energy can be a float number or a stdVector.StdVector instance
##     
##
class He3DetEffic( Base):
    
    """Functor to compute energy dependence of efficiency of 3He detector."""

    def nPoints( self):
        """nPoints() -> number of grid points in integration"""
        return self._nPoints


    def pressure( self):
        """pressure() -> He3 pressure of detector (in atmospheres)"""
        return self._pressure
    

    def radius( self):
        """radius() -> radius of detector (in mm)"""
        return self._radius

    
    def __call__(self, energy, output=None):
        """he3DetEffic( energy, output=None)->varies
        Compute the efficiency(ies) for the given energy(ies).
        Input(s):
            energy: in meV and > 0, either a single float, or a StdVector
            output: optional StdVector for output (see notes)
        Output:
            case 1: if energy is a single float, returns a single float
            case 2: if energy is a StdVector, returns a StdVector. If user
                    provided an output vector, that vector is returned.
        Exceptions: ValueError
        Notes: (1) If using vectors, all vectors must be of the same type as
        this efficiency calculator.
        (2) If using vectors and no output vector is provided, one will be
        created for you. This is potentially time consuming. """
        #if energy.__class__.__name__ in [ "StdVector", "NdArray" ]:
        if energy.__class__.__name__ == 'NdArray':
            energy = energy.as( vectorType )
            if energy.datatype() != self.datatype():
                raise TypeError,"Energy type (%s) different"%energy.datatype()
            if not output:
                from stdVector import vector
                output = vector( self.datatype(), energy.size())
            else:
                if output.datatype() != self.datatype():
                    msg = "Output type (%s) different"%energy.datatype()
                    raise TypeError, msg
                
            red.He3LPSDEffic_callVector( self.handle(), self.datatype(),
                                         energy.handle(), output.handle())
        else:
            output = red.He3LPSDEffic_callSingle( self._handle,
                                                  self._templateType, energy)
        return output


    def __init__(self, pressure, radius, nPoints=500, dtype=6):
        """He3LPSDEffic( pressure, radius, nPoints=500, dtype=6)->new He3DetEffic
        Create an object that calculates the efficiency of a He3 detector as a
        function of energy.
        Inputs:
            pressure: of He3 in atmospheres (float)
            radius: of detector tube in cm (float)
            nPoints: number points used in integral
            dtype: type code, 5.....float, 6.....double
        Outputs:
            new He3LPSDEffic object
        Exceptions: ValueError, RuntimeError
        Notes: (1) See documentation for details of passing to and receiving in
        C++.
        (2) ValueError on unrecognized data type.
        (3) RuntimeError if unable to create/allocate."""

        debug.log( "create He3 detector efficiency calculator: pressure is %s atm, radius is %s cm" % (pressure, radius) )
        handle = red.He3LPSDEffic( dtype, pressure, radius, nPoints)
        classID = red.He3LPSDEffic_classID()
        Base.__init__( self, dtype, handle, "He3DetEffic<T>", classID)

        self._pressure  = pressure
        self._radius = radius
        self._nPoints = nPoints
        
        return


    pass # end of He3DetEffic

vectorType = "StdVectorNdArray"


# version
__id__ = "$Id: He3DetEffic.py 1401 2007-08-29 15:36:44Z linjiao $"

# End of file
