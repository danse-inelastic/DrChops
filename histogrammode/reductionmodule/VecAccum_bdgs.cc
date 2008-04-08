// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "VecAccum_bdgs.h"
#include "VecAccum.h"
#include "reduction/utils.h"
#include "stdVector/utils.h"
#include <valarray> // for std::slice 
#include "journal/debug.h"

namespace reductionmod
{
  namespace 
  {
    using journal::at;
    using journal::endl;
    char journalname [] = "reductionmod";
        
    template <typename FPT>
    bool _callVecAccum( PyObject *pytarget, PyObject *pysource, int dtype,
			std::slice &slice)
    {
      journal::debug_t debug( journalname);

      // unwrap vectors
      std::vector<FPT> *psrc =
	ARCSStdVector::unwrapVector<FPT> ( pysource, dtype);
      if( psrc == 0)
	{
	  debug << at(__HERE__) << "unwrap vector failed for source"
		<< endl;
	  return false;  // exception context set in unwrapVector
	}

      std::vector<FPT> *ptarg =
	ARCSStdVector::unwrapVector<FPT> ( pytarget, dtype);
      if( ptarg == 0)
	{
	  debug << at(__HERE__) << "unwrap vector failed for source"
		<< endl;
	  return false;  // exception context set in unwrapVector
	}

      // create a VecAccum<FPT>
      typedef  DANSE::Reduction::VecAccum<FPT> w_t;

      w_t accum( *ptarg);
      try
	{
	  accum( *psrc, slice);
	}
      catch( std::string &errstr)
	{
	  debug << at(__HERE__) 
		<< "Caught exception from VecAccum::operator(): "
		<< errstr.c_str();
	  PyErr_SetString( PyExc_IndexError, errstr.c_str());
	  return false;
	}
      return true;
    }
  } // anonymous

  char VecAccum__name__[] = "accumulate";
  char VecAccum__doc__[] =
    "VecAccum( targetVector, sourceVector, datatype, slice) -> None\n"
    "add sourceVector to targetVector as per slice\n"
    "Inputs:\n"
    "    targetVector: StdVector handle\n"
    "    sourceVector: StdVector handle\n"
    "    datatype: type code\n"
    "    slice: std::slice instance\n"
    "Output:\n"
    "    None\n"
    "Exceptions: ValueError, RuntimeError.\n"
    "Notes: None.";

  PyObject * VecAccum(PyObject *, PyObject *args)
  {
    PyObject *pytarget, *pysource, *pySlice;
    int dtype = 0;
    int ok = PyArg_ParseTuple( args, "OOiO",  &pytarget, &pysource, &dtype,
			       &pySlice);
    if(!ok) return 0;

    std::string errstr("reductionmod::VecAccum() ");

    bool okay = true;
    journal::debug_t debug( journalname);

    std::slice *pslice =
      DANSE::Reduction::utils::unwrapObject<std::slice>( pySlice, 0);

    if( pslice == 0)
      {
	debug << at(__HERE__) << "unwrap slice failed" << endl;
	return 0;  // exception context set in unwrapObject
      }
    switch( dtype)
      {
      case 5:   // float
	okay = _callVecAccum<float>( pytarget, pysource, dtype, *pslice);
	break;
      case 6:   // double
	okay = _callVecAccum<double>( pytarget, pysource, dtype, *pslice);
	break;
      default:
	errstr += "unrecognized datatype, recognized types are:\n"
	  "    5.......float\n"
	  "    6.......double\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      } // switch( ...)
        
    if( !okay)
      {
	return 0; // exception context set in subroutine
      }

    Py_INCREF( Py_None);
    return Py_None;
  }


} // reductionmod


// version
// $Id: VecAccum_bdgs.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
