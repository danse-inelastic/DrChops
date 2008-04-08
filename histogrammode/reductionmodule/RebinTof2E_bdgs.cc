// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <sstream>
#include <iostream>

#include "reduction/utils.h"
#include "numpy_support.h"
#include "RebinTof2E_bdgs.h"

#include "reduction/RebinTof2E.h"


namespace reductionmod
{

  typedef DANSE::Reduction::RebinTof2E<double, const double *, double *> Rebinner_usepointers;
  typedef Array1DIterator<npy_double> DblArrIt;
  typedef DANSE::Reduction::RebinTof2E<npy_double, DblArrIt, DblArrIt > Rebinner_usenumpy;

  using DANSE::Reduction::utils::deleteHeapObj;

  // constructor
  char RebinTof2E__name__[] = "RebinTof2E";
  char RebinTof2E__doc__[] = "Constructor of RebinTof2E\n"\
    "RebinTof2E( distance ) \n"\
    "distance: mm\n";

  PyObject * RebinTof2E(PyObject *, PyObject *args)
  {
    npy_double distance = 0.0;

    int ok = PyArg_ParseTuple( args, "d", &distance);
    if (!ok) return 0;

    std::string errstr("RebinTof2E() ");

    Rebinner_usenumpy *rebinner = new Rebinner_usenumpy( distance );

    return PyCObject_FromVoidPtr( rebinner, deleteHeapObj<Rebinner_usenumpy>);
  }
    

  // __call__
  char RebinTof2ECall_numpyarray__name__[] = "RebinTof2E__call__numpyarray";
  char RebinTof2ECall_numpyarray__doc__[] = \
    "RebinTof2E__call__numpyarray( rebinner, tofarray, Itofarray, tmpEarray,\n"\
    "                    Earray, IEarray )\n" ;
  extern "C"
  PyObject * RebinTof2ECall_numpyarray(PyObject *, PyObject *args)
  {

    PyObject *pytof, *pyItof, *pytmpE, *pyE, *pyIE;
    PyObject *pyrebinner;
    
    int ok = PyArg_ParseTuple( args, "OOOOOO", &pyrebinner, &pytof, &pyItof,
			       &pytmpE, &pyE, &pyIE);
    if (!ok) return 0;

    if (checkDataType(pytof, "tof", NPY_DOUBLE)) return 0;
    if (checkDataType(pyItof, "Itof", NPY_DOUBLE)) return 0;
    if (checkDataType(pytmpE, "tmpE", NPY_DOUBLE)) return 0;
    if (checkDataType(pyE, "E",  NPY_DOUBLE)) return 0;
    if (checkDataType(pyIE, "IE",  NPY_DOUBLE)) return 0;

    DblArrIt tofBegin (pytof), tofEnd = tofBegin + PyArray_Size(pytof);
    //print(tofBegin, tofEnd);

    DblArrIt ItofBegin(pyItof);
    //print(ItofBegin, ItofBegin + PyArray_Size(pytof)-1);

    DblArrIt tmpEBegin(pytmpE);
    DblArrIt EBegin( pyE ), EEnd = EBegin + PyArray_Size(pyE);
    //print(EBegin, EEnd);

    DblArrIt IEBegin(pyIE);
    //print(IEBegin, IEBegin + PyArray_Size(pyE)-1);

    Rebinner_usenumpy *rebinner = (Rebinner_usenumpy*) 
      PyCObject_AsVoidPtr( pyrebinner );

    (*rebinner)( tofBegin, tofEnd, ItofBegin,
		 tmpEBegin,
		 EBegin, EEnd, IEBegin );
    
    return Py_None;
  }

  
} // reductionmod::



// version
// $Id: RebinTof2E_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
