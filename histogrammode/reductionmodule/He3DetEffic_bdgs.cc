// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "He3DetEffic_bdgs.h"
#include "He3DetEffic.h"

#include "reduction/utils.h"
#include "stdVector/utils.h"
#include "journal/debug.h"
#include <vector>
#include <sstream>
#include <iostream>
#include <string>


namespace reductionmod
{
  int He3DetEffic__magicNumber = 602458330;

  char He3DetEffic__name__[] = "He3LPSDEffic";
  char He3DetEffic__doc__[] = 
    "He3DetEffic( pressure, radius, numnPoints, costheta)\n"
    "Create a new He3DetEffic object, which computes the energy dependence \n"
    "of a 3-He detector's absorption\n"
    "Inputs:\n"
    "    dtype: type code. Recognized types are \n"
    "        5.......float\n"
    "        6.......double\n"
    "    pressure: in atmospheres (floating point)\n"
    "    radius: in cm (floating point)\n"
    "    numPoints: number points to use in grid, must be > 0\n"
    "    costheta: cos(theta), theta being angle between kf  and scattering plane"
    "Output: \n"
    "    New He3DetEffic instance\n"
    "Exceptions: ValueError\n"
    "Notes: (1) To unwrap in C++, use utils::unwrapObject<He3DetEffic<FPT> >.";


  namespace
  {
    template <typename T>
    bool _checkArgPositive( T arg, std::stringstream &errstr)
    {
      if (arg > (T)0) return true;
      else
	{
	  errstr << "value must be > 0, was " << arg;
	  PyErr_SetString( PyExc_ValueError, errstr.str().c_str());
	  return false;
	}
    }

    template <typename FPT>
    PyObject *_callCtor( int dtype, FPT press, FPT radius, 
			 unsigned nPoints, FPT costheta)
    {
      typedef typename std::vector<FPT>::iterator FPTIt;
      typedef DANSE::Reduction::He3DetEffic<FPT, FPTIt> w_t;
      
      w_t *newde = 
	new w_t( press, radius, nPoints, costheta);

      return DANSE::Reduction::utils::wrapObject<w_t>
	(newde, dtype, reductionmod::He3DetEffic__magicNumber);
    }

  } // anonymous::


  PyObject * He3DetEffic(PyObject *, PyObject *args)
  {
    int dtype = 0;
    double press = 0.0, radius = 0.0, costheta=1.0;
    unsigned nPoints = 0;
    int ok = PyArg_ParseTuple( args, "iddI|d", &dtype, &press, &radius,
			       &nPoints, &costheta);
    if (!ok) return 0;
    
    std::stringstream errstr("He3DetEffic(): ");

    // subroutine sets exception context
    if (! _checkArgPositive<double>( press, errstr)) return 0;
    if (! _checkArgPositive<double>( radius, errstr)) return 0;
    if (! _checkArgPositive<unsigned>( nPoints, errstr)) return 0;
    if (! _checkArgPositive<double>( costheta, errstr)) return 0;

    PyObject *retval = 0;

    switch( dtype)
      {
      case 5:    // float
	retval = _callCtor<float>( dtype, (float)press, (float)radius, 
				   nPoints, (float)costheta);
	break;
      case 6:   // double
	retval = _callCtor<double>( dtype, press, radius, nPoints, costheta);
	break;
      default:
	errstr << "unrecognized type code " << dtype 
	       << ". Recognized types are\n"
	       << "    5.......float\n"
	       << "    6.......double\n";
	PyErr_SetString( PyExc_ValueError, errstr.str().c_str());
      } // switch

    return retval;
  }  // He3DetEffic


  char He3DetEfficExecSingle__name__[] = "He3LPSDEffic_callSingle";
  char He3DetEfficExecSingle__doc__[] = 
    "He3LPSDEffic_CallSingle( He3DetEffic, dtype, energy)\n"
    "computes efficiency for a single energy\n"
    "inputs:\n"
    "    He3DetEffic (PyCObject/void ptr)\n"
    "    energy (floating point >=0.0, in meV)\n"
    "outputs: efficiency (floating point, dimensionless)\n"
    "Exceptions: ValueError";


  namespace 
  {
    template <typename FPT>
    double _callDetEffic( int dtype, PyObject *pyde, double energy)
    {
      typedef typename std::vector<FPT>::iterator FPTIt;
      typedef DANSE::Reduction::He3DetEffic<FPT, FPTIt > w_t;

      w_t *pde = 
	DANSE::Reduction::utils::unwrapObject<w_t >(pyde, dtype);

      if ( pde==0)
	{
	  std::string errstr("unwrap failed");
	  throw( errstr);
	}

      return (double)pde->operator()( (FPT)energy);
    }

  } // anonymous::


  PyObject * He3DetEfficExecSingle(PyObject *, PyObject *args)
  {
    PyObject *pyde = 0;
    double energy = 0.0;
    int dtype = 0;
    int ok = PyArg_ParseTuple( args, "Oid", &pyde, &dtype, &energy);
    if (!ok) return 0;

    std::stringstream errstr( "He3DetEfficExecSingle");

    if (! _checkArgPositive<double>( energy, errstr)) return 0;

    double retval = 0.0;

    try
      {
	switch( dtype)
	  {
	  case 5:   // float
	    retval = _callDetEffic<float>( dtype, pyde, energy);
	    break;
	  case 6:   // double
	    retval = _callDetEffic<double>( dtype, pyde, energy);
	    break;
	  default:
	    errstr << "Unrecognized type code " << dtype << ". Recognized "
		   << "codes are: 5....float, 6....double\n";
	    PyErr_SetString( PyExc_ValueError, errstr.str().c_str());
	    return 0;
	  } // switch( dtype)
      } // try
    catch( std::string &)
      {
	// exception context set by unwrapObject
	return 0;
      }

    return Py_BuildValue("d", retval);
  } // He3DetEfficExecSingle(...)



  char He3DetEfficExecVector__name__[] = "He3LPSDEffic_callVector";
  char He3DetEfficExecVector__doc__[] = 
    "He3DetEffic_callVector( He3DetEffic, dtype, stdVectorEnergies, stdVectorResult)\n"
    "Compute efficiencies for a vector of energies\n"
    "Inputs:\n"
    "    He3DetEffic: efficiency calcor object\n"
    "    dtype: floating-point type of this object\n"
    "    stdVectorEnergies: std::vector<dtype> instance with energies\n"
    "    stdVectorEfficiencies: std::vector<dtype> instance to hold output\n"
    "Output:\n"
    "    None\n"
    "Exceptions: ValueError\n";

  namespace
  {
    template <typename FPT>
    bool _callDetEfficVect( int dtype, PyObject *pyde, PyObject *pynrg,
			    PyObject *pyeffic)
    {
      typedef typename std::vector<FPT> w_vec;
      typedef typename w_vec::iterator FPTIt;
      typedef DANSE::Reduction::He3DetEffic<FPT, FPTIt > w_t;

      w_t *pde = 
	DANSE::Reduction::utils::unwrapObject<w_t >(pyde, dtype);
      if ( pde==0)
	{
	  return false;
	}
      w_vec *pnrg = 
	ARCSStdVector::unwrapVector<FPT>( pynrg, dtype);
      if ( pnrg==0)
	{
	  return false;
	}

      w_vec *peffic = 
	ARCSStdVector::unwrapVector<FPT>( pyeffic, dtype);
      if ( peffic==0)
	{
	  return false;
	}
      (*pde)( pnrg->begin(), peffic->begin(), peffic->end() );
      return true;
    }
        
  } // anonymous::


  PyObject *He3DetEfficExecVector(PyObject *, PyObject *args)
  {
    int dtype = 0;
    PyObject *pyhde = 0, *pynrg = 0, *pyeffic = 0;

    int ok = PyArg_ParseTuple( args, "OiOO", &pyhde, &dtype, &pynrg, 
			       &pyeffic);
    if(!ok) return 0;

    bool okay = true;
    switch( dtype)
      {
      case 5:    // float
	okay = _callDetEfficVect<float>( dtype, pyhde, pynrg, pyeffic);
	if(! okay) return 0;
	break;
      case 6:
	okay = _callDetEfficVect<double>( dtype, pyhde, pynrg, pyeffic);
	if(! okay) return 0;
	break;
      default:
	std::stringstream errstr;
	errstr << __FILE__ << " " << __LINE__ 
	       << "He3DetEfficExecVector(): Unrecognized type code "
	       << dtype 
	       << ". Recognized types are 5....float, 6....double";
	PyErr_SetString( PyExc_ValueError, errstr.str().c_str());
	return 0;
      } // switch(...)


    Py_INCREF( Py_None);
    return Py_None;
  } // He3DetEfficExecVector(...)

    
    //---------------------------- classID -------------------------------

  char He3DetEffic_classID__name__[] = "He3LPSDEffic_classID";
  char He3DetEffic_classID__doc__[] = 
    "He3LPSDEffic_classID() -> classID\n"
    "Get magic number used in wrapping this class\n"
    "Inputs:\n"
    "    None\n"
    "Outputs:\n"
    "    classID (integer)\n"
    "Exceptions: None\n";

  PyObject *He3DetEffic_classID( PyObject *, PyObject *args)
  {
    return Py_BuildValue( "i", He3DetEffic__magicNumber);
  }


} // reductionmod


// version
// $Id: He3DetEffic_bdgs.cc 1443 2007-11-15 07:17:37Z linjiao $

// End of file
