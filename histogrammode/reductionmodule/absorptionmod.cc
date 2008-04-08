// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2003-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//



#include "absorptionmod.h"
#include "VanPlateAbsorp.h"
#include <string>
#include "journal/debug.h"
#include "reduction/utils.h"


namespace
{
  using journal::at;
  using journal::endl;
  const char journalname [] = "reductionmod";

  bool _checkPositive( double arg, std::string & errstr)
  {
    if ( arg >= 0.0) return true;
    else
      {
	errstr += "arg must be positive";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return false;
      }
  }
} // anonymous::


namespace reductionmod
{
  int vanPlateXmission__magicNumber__ = 29438502;

  char vanPlateXmission_ctor__name__[] = "vanPlateXmission_ctor";
  char vanPlateXmission_ctor__doc__[] = 
    "vanPlateXmission_ctor( darkAngle, thickness, width)\n"
    "Create functor to compute the transmission through a Vanadium plate.\n"
    "inputs:\n"
    "    darkAngle (angle from tranmitted beam to long axis of plate, viewed\n"
    "               from above, in degrees; float)\n"
    "    thickness (of plate, in cm; float)\n"
    "    width (in cm (dimension parallel to dark-angle axis); float)\n"
    "outputs:\n"
    "    PyCObject/void ptr to new object\n"
    "Exceptions: ValueError";

  PyObject * vanPlateXmission_ctor(PyObject *, PyObject *args)
  {
    double darkAngle = 0.0, thickness = 0.0, width = 0.0;
    int ok = PyArg_ParseTuple( args, "ddd", &darkAngle, &thickness, 
			       &width);
    if (!ok) return 0;

    std::string errstr("vanPlateXmission_ctor(): ");
    journal::debug_t debug( journalname);

    // Exception context set in subroutine
    if(! _checkPositive(thickness, errstr)) return 0;
    if(! _checkPositive(width, errstr))     return 0;

    using namespace DANSE::Reduction;

    VanPlateAbsorp *newvpa = 0;
    try
      {
	newvpa = 
	  new VanPlateAbsorp( darkAngle, thickness, width);
      }
    catch( std::bad_alloc & ba)
      {
	errstr += "Failed to allocate VanPlateAbsorp";
	debug << at(__HERE__) << errstr << endl;
	PyErr_SetString( PyExc_RuntimeError, errstr.c_str());
	return 0;
      }
    PyObject *retval = 
      utils::wrapObject<VanPlateAbsorp>( 
					newvpa, 0, vanPlateXmission__magicNumber__);
    if( retval == 0)
      {
	delete newvpa;
	errstr += "TWrapper FAILED";
	debug << at(__HERE__) << errstr.c_str() << endl;
	// exception context set in wrapObject
	return 0;
      }

    return retval;
  } // vanPlateXmission_ctor( ... )


    // VanPlateXmissionCall methods
  char vanPlateXmission_call__name__[] = "vanPlateXmission_call";
  char vanPlateXmission_call__doc__[] = 
    "VanPlateXmission_call( vanPlateXmission, detectorAngle, energy)\n"
    "compute transmission for given energy and scattering angle\n"
    "inputs:\n"
    "    vanPlateXmission (VanPlateXmission object; PyCObject/void ptr)\n"
    "    detectorAngle (in degrees; float)\n"
    "    energy (in meV, must be > 0; float)\n"
    "outputs: transmission coefficient (float)\n"
    "Exceptions: ValueError";

  PyObject * vanPlateXmission_call(PyObject *, PyObject *args)
  {
    PyObject *pyvpa = 0;
    double detectorAngle = 0.0, energy = 0.0;
    int ok = PyArg_ParseTuple( args, "Odd", &pyvpa, &detectorAngle, 
			       &energy);
    if (!ok) return 0;

    std::string errstr("pyreduction_VanPlateXmission_call(): ");
    journal::debug_t debug( journalname);

    // Exception context set in subroutine
    if(! _checkPositive( energy, errstr)) return 0;
    
    using namespace DANSE::Reduction;

    VanPlateAbsorp *thisvpa = 
      utils::unwrapObject<VanPlateAbsorp>(
					  pyvpa, 0);

    if( thisvpa == 0)
      {
	errstr += "unwrap TWrapper FAILED";
	debug << at(__HERE__) << errstr.c_str() << endl;
	// exception context set in unwrapObject
	return 0;
      }

    double tx = thisvpa->operator()(detectorAngle, energy);
    return Py_BuildValue("d", tx);
  }

} // reductionmod::

// version
// $Id: absorptionmod.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
