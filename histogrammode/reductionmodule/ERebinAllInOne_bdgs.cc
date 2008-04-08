// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "ERebinAllInOne_bdgs.h"
#include "reduction/ERebinAllInOne.h"

#include "stdVector/utils.h"
#include "reduction/utils.h"

#include <vector>
#include <string>

namespace reductionmod
{
  const int ERebinAllInOne__magicNumber__ = 304991278;

  char ERebinAllInOne_ctor__name__[] = "ERebinAllInOne_ctor";
  char ERebinAllInOne_ctor__doc__[] = 
    "ERebinAllInOne_ctor( dtype, nOldBins, nNewBins, dtOverde, doKPOK, ei)\n"
    "Create a new ERebinAllInOne object\n"
    "Inputs:\n"
    "    dtype: (int) Recognized typecodes:\n"
    "        5......float\n"
    "        6.....double\n"
    "    nOldBins: Number of bins in old histogram\n"
    "    nNewBins: Number of bins in new histogram\n"
    "    dtOverde: delta-t divided by delta-e\n"
    "    doKPOK: (0=>no; 1=>yes) whether to apply k-prime over k correction\n"
    "    ei: (float) incident energy in meV\n"
    "Output:\n"
    "    new ERebinAllInone instance wrapped by utils::wrapObject.\n"
    "Exceptions: ValueError (bad datatype)\n"
    "Notes: use utils::unwrapObject<DANSE::Reduction::ERebinAllInOne> to recover\n"
    "pointer to object.";
}

namespace
{
  using DANSE::Reduction::ERebinAllInOne;

  template <typename FPT>
  PyObject * callERB_ctor( int dtype, size_t nold, size_t nnew,
			   FPT dtOverde, bool doKPOK, FPT ei)
  {
    ERebinAllInOne<FPT> *perb = new ERebinAllInOne<FPT>
      (nold, nnew, dtOverde, doKPOK, ei);

    return DANSE::Reduction::utils::wrapObject< ERebinAllInOne<FPT> >
      (perb, dtype, reductionmod::ERebinAllInOne__magicNumber__);
  }
} // anonymous::

namespace reductionmod
{
  PyObject * ERebinAllInOne_ctor(PyObject *, PyObject *args)
  {
    int dtype = 0, idoKPOK = 0;
    unsigned nnew = 0, nold = 0;
    double dtOverde = 1.0, ei = 0.0;
    int ok = PyArg_ParseTuple( args, "iIId|id", &dtype, &nold, &nnew, 
			       &dtOverde, &idoKPOK, &ei);
    if (!ok) return 0;

    std::string errstr( "DANSE::Reduction::ERebinAllInOne_ctor() ");

    bool doKPOK = (idoKPOK == 0) ? false : true;

    switch( dtype)
      {
      case 5: // float
	return callERB_ctor< float>( dtype, nold, nnew, (float) dtOverde, 
				     doKPOK, (float) ei);
      case 6: // double
	return callERB_ctor< double>( dtype, nold, nnew, dtOverde, 
				      doKPOK, ei);
      default:
	errstr += "Unrecognized data type. Recognized types are:\n"
	  "    float......5\n"
	  "    double.....6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      } // switch( dtype)
  }


  char ERebinAllInOne_call__name__[] = "ERebinAllInOne_call";
  char ERebinAllInOne_call__doc__[] = 
    "ERebinAllInOne_call(dtype, eRebinAllInOne, oldBins, newBins, inData, inErrors, outData, outErrors)\n"
    "Call ERebinAllInOne object to rebin data & errors.\n"
    "Inputs:\n"
    "    dtype: datatype of ERebinAllInOne object\n"
    "    eRebinAllInOne: object as wrapped by utils::wrapObject\n"
    "    oldBins: (stdVector handle) old bin boundaries\n"
    "    newBins: (stdVector handle) new bin boundaries\n"
    "    inData: (stdVector handle) input data\n"
    "    inErrors: (stdVector handle) input errors\n"
    "    outData: (stdVector handle) output data\n"
    "    outErrors: (stdVector handle) output errors\n"
    "Output:\n"
    "    None\n"
    "Exceptions: ValueError, TypeError\n"
    "Notes: datatype of all vectors must match that of the ERebinAllInOne \n"
    "object.";

} // reductionmod::


namespace
{
  template <typename T>
  bool _checkPtr( T *pt, std::string &errstr)
  {
    if (pt == 0)
      {
	errstr += "Failed to unwrap object.\n";
	return false;
      }
    else
      {
	errstr += "unwrap ok\n";
	return true;
      }
  }

  template <typename FPT>
  bool callERB_call( int dtype, PyObject *pyERB, PyObject *pyoldb,
		     PyObject *pynewb, PyObject *pyindata, 
		     PyObject *pyinerrs, PyObject *pyoutdata,
		     PyObject *pyouterrs, std::string &errstr)
  {
    using ARCSStdVector::unwrapVector;
    using namespace DANSE::Reduction;

    ERebinAllInOne<FPT> *perb = 
      utils::unwrapObject< ERebinAllInOne<FPT> >( 
						 pyERB, dtype);
    if( ! _checkPtr<ERebinAllInOne<FPT> >(perb, errstr)) return false;

    std::vector<FPT> *poldb = unwrapVector<FPT>( pyoldb, dtype);
    if( ! _checkPtr<std::vector<FPT> >(poldb, errstr)) return false;
    std::vector<FPT> *pnewb = unwrapVector<FPT>( pynewb, dtype);
    if( ! _checkPtr<std::vector<FPT> >(pnewb, errstr)) return false;

    std::vector<FPT> *pindata = unwrapVector<FPT>( pyindata, dtype);
    if( ! _checkPtr<std::vector<FPT> >(pindata, errstr)) return false;
    std::vector<FPT> *pinerrs = unwrapVector<FPT>( pyinerrs, dtype);
    if( ! _checkPtr<std::vector<FPT> >(pinerrs, errstr)) return false;

    std::vector<FPT> *poutdata = unwrapVector<FPT>( pyoutdata, dtype);
    if( ! _checkPtr<std::vector<FPT> >(poutdata, errstr)) return false;
    std::vector<FPT> *pouterrs = unwrapVector<FPT>( pyouterrs, dtype);
    if( ! _checkPtr<std::vector<FPT> >(pouterrs, errstr)) return false;

    perb -> operator()( *poldb, *pnewb, *pindata, *pinerrs,
			*poutdata, *pouterrs);
    return true;
  }

} // anonymouse::

namespace reductionmod
{
  PyObject * ERebinAllInOne_call(PyObject *, PyObject *args)
  {
    int dtype = 0;
    PyObject *pyERB = 0;
    PyObject *pyoldb = 0, *pynewb = 0, *pyindata = 0;
    PyObject *pyinerrs = 0, *pyoutdata = 0, *pyouterrs = 0;
    int ok = PyArg_ParseTuple( args, "iOOOOOOO", &dtype, &pyERB, &pyoldb,
			       &pynewb, &pyindata, &pyinerrs, &pyoutdata,
			       &pyouterrs);
    if(!ok) return 0;

    std::string errstr("DANSE::Reduction::ERebinAllInOne_call() ");

    switch( dtype)
      {
      case 5:    // float
	if( !callERB_call<float>( dtype, pyERB, pyoldb, pynewb, pyindata, 
				  pyinerrs, pyoutdata,pyouterrs,errstr))
	  return 0;
	break;
      case 6:    // double
	if( !callERB_call<double>( dtype, pyERB, pyoldb, pynewb, pyindata, 
				   pyinerrs,pyoutdata,pyouterrs,errstr))
	  return 0;
	break;
      default:
	errstr += "Unrecognized data type. Recognized types are:\n"
	  "    float......5\n"
	  "    double.....6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      } // switch( dtype)

    Py_INCREF(Py_None);
    return Py_None;
  } // ERebinAllInOne_call( ...)


} // reductionmod::



// version
// $Id: ERebinAllInOne_bdgs.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
