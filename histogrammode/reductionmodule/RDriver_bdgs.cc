// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "RDriver_bdgs.h"
#include "reduction/RDriver.h"
#include "reduction/utils.h"
#include "stdVector/utils.h"

#include "journal/debug.h"

namespace reductionmod
{
  int RDriver__magicNumber__ = 906517712;

  namespace
  {
    using journal::at; using journal::endl;
    char journalname [] = "reductionmod.RDriver";


    template <typename NumT>
    PyObject* _callRDriver_ctor( PyObject *pyspevec, int dtype,
				 size_t otherlen, PyObject *pyphiBBvec)
    {
      journal::debug_t debug( journalname);

      std::vector<NumT> *pspe = 
	ARCSStdVector::unwrapVector<NumT> (pyspevec, dtype);
      if( pspe == 0)
	{
	  debug << at(__HERE__) << "unwrap vector failed, spe" << endl;
	  return 0;
	}

      std::vector<NumT> *pphiBB = 
	ARCSStdVector::unwrapVector<NumT> (pyphiBBvec, dtype);
      if( pphiBB == 0)
	{
	  debug << at(__HERE__) << "unwrap vector failed, phiBB" << endl;
	  return 0;
	}

      typedef DANSE::Reduction::RDriver<NumT> w_t;

      w_t *newrd = 0;
      try
	{
	  newrd = new w_t( *pspe, otherlen, 
				     *pphiBB);
	}
      catch ( std::bad_alloc &ba)
	{
	  debug << at(__HERE__) << "allocation failed" << ba.what() 
		<< endl;
	  PyErr_SetString( PyExc_RuntimeError, ba.what());
	  return 0;
	}

      PyObject *retval = DANSE::Reduction::utils::wrapObject< 
      w_t > ( newrd, dtype, 
			RDriver__magicNumber__);
      if( retval == 0)
	{
	  debug << at(__HERE__) << "wrapObject failed" << endl;
	}
      return retval;
    } //_callRDriver_ctor
  } // anonymous::

  char RDriver__name__[] = "RDriver";
  char RDriver__doc__[] = 
    "RDriver( speVector, datatype, otherArrLen, phiBBVec)--> RDriver\n"
    "Create a new driver object for summing by scattering angle.\n"
    "inputs:\n"
    "    speVector ..(std::vector<datatype>; PyCObject)\n"
    "    datatype ...(int, see below for supported types/codes)\n"
    "    otherArrLen (length of other (non-phi) array dimension)\n"
    "    phiBBVec ...(phi bin bdy vals, degrees; std::vector<datatype>/PyCObject\n)"
    "output:\n"
    "    RDriver instance, PyCObject\n"
    "Exceptions: ValueError\n"
    "Notes: Recognized datatypes:\n"
    "          float....5\n"
    "          double...6\n";

  PyObject * RDriver(PyObject *, PyObject *args)
  {
    PyObject *pyspevec = 0, *pyphiBB = 0;
    int dtype = 0;
    int sotherlen = 0;
    int ok = PyArg_ParseTuple( args, "OiiO", &pyspevec, &dtype, &sotherlen,
			       &pyphiBB);
    if (!ok) return 0;

    std::string errstr("RDriver() ");
    if (sotherlen < 1)
      {
	errstr += "otherArrLen must be > 0";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    size_t otherlen = static_cast<size_t>(sotherlen);
    switch (dtype)
      {
      case 5:   // float
	return _callRDriver_ctor<float> ( pyspevec, dtype, otherlen, 
					  pyphiBB);
      case 6:   // double
	return _callRDriver_ctor<double>( pyspevec, dtype, otherlen, 
					  pyphiBB);
      default:
	errstr += "unrecognized datatype. Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
      }
    return 0;
  }

  namespace
  {
    template <typename NumT>
    bool _callRDriver_call( PyObject *pyrd, PyObject *pysrcvec, int dtype,
			    double scatteringAngle)
    {
      journal::debug_t debug( journalname);

      std::vector<NumT> *psrc = 
	ARCSStdVector::unwrapVector<NumT> (pysrcvec, dtype);
      if(psrc == 0)
	{
	  debug << at(__HERE__) << "unwrap vector failed" << endl;
	  return false;
	}

      typedef DANSE::Reduction::RDriver<NumT> w_t;

      w_t *prd = 
	DANSE::Reduction::utils::unwrapObject< w_t >(
					     pyrd, dtype);
      if( prd == 0)
	{
	  debug << at(__HERE__) << "unwrapObject failed" << endl;
	  return false;
	}
      prd->ring( *psrc, scatteringAngle);
      return true;
    } // _callRDriver_call
  } // anonymous::

  char RDriver_call__name__[] = "RDriver_call";
  char RDriver_call__doc__[] = 
    "RDriver_call( RDriver, datatype, sourceVec, scatteringAngle)--> None\n"
    "Create a new driver object for summing by scattering angle.\n"
    "inputs:\n"
    "    RDriver instance (PyCObject)\n"
    "    datatype ........(int, see below for supported types/codes)\n"
    "    sourceVector ....(std::vector<datatype>; PyCObject)\n"
    "    scatteringAngle ...........(float)\n"
    "output: None"
    "Exceptions: ValueError\n"
    "Notes: Recognized datatypes:\n"
    "          float....5\n"
    "          double...6\n";

  PyObject * RDriver_call(PyObject *, PyObject *args)
  {
    PyObject *pyrd = 0, *pysrcvec = 0;
    double scatteringAngle = 0.0;
    int dtype = 0;
    int ok = PyArg_ParseTuple( args, "OiOd", &pyrd, &dtype, &pysrcvec, 
			       &scatteringAngle);
    if (!ok) return 0;

    std::string errstr("RDriver_call() ");

    switch (dtype)
      {
      case 5:   // float
	_callRDriver_call<float> ( pyrd, pysrcvec, dtype, scatteringAngle);
	break;
      case 6:   // double
	_callRDriver_call<double>( pyrd, pysrcvec, dtype, scatteringAngle);
	break;
      default:
	errstr += "unrecognized datatype. Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    Py_INCREF(Py_None);
    return Py_None;
  }


  namespace details
  {
    template <typename NumT>
    bool _callRDriver_norms( PyObject *pyrd, PyObject *pynorms, int dtype )
    {
      journal::debug_t debug( journalname);

      typedef DANSE::Reduction::RDriver<NumT> w_t;
      
      w_t *prd = 
	DANSE::Reduction::utils::unwrapObject< w_t >(
					     pyrd, dtype);
      if( prd == 0)
	{
	  debug << at(__HERE__) << "unwrapObject failed" << endl;
	  return false;
	}

      std::vector<NumT> *pnorms = 
	ARCSStdVector::unwrapVector<NumT>( pynorms, dtype);
      if ( pnorms==0)
	{
	  debug << at(__HERE__) << "unwrap std::vector failed" << endl;
	  return false;
	}
	    
      const std::vector<NumT> & norms = prd->norms();
      *pnorms = norms;
      return true;
    } // _callRDriver_call
  } // details::


  char RDriver_norms__name__[] = "RDriver_norms";
  char RDriver_norms__doc__[] = 
    "RDriver_norms( RDriver, norms, datatype)--> None\n"
    "return norms of given RDriver into given vector norms \n"
    "inputs:\n"
    "    RDriver instance (PyCObject)\n"
    "    datatype ........(int, see below for supported types/codes)\n"
    "    norms....... ....(std::vector<datatype>; PyCObject)\n"
    "output: None"
    "Exceptions: ValueError\n"
    "Notes: Recognized datatypes:\n"
    "          float....5\n"
    "          double...6\n";

  PyObject * RDriver_norms(PyObject *, PyObject *args)
  {
    PyObject *pyrd = 0, *pynorms = 0;
    int dtype = 0;
    int ok = PyArg_ParseTuple( args, "OOi", &pyrd, &pynorms, &dtype);
    if (!ok) return 0;

    std::string errstr("RDriver_norms() ");

    switch (dtype)
      {
      case 5:   // float
	details::_callRDriver_norms<float> ( pyrd, pynorms, dtype );
	break;
      case 6:   // double
	details::_callRDriver_norms<double>( pyrd, pynorms, dtype );
	break;
      default:
	errstr += "unrecognized datatype. Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    Py_INCREF(Py_None);
    return Py_None;
  }


} // reductionmod

// version
// $Id: RDriver_bdgs.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
