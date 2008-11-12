// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                      (C) 2007-2008  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#include <sstream>
#include <iostream>

#include "utils.h"
#include "numpy_support.h"
#include "Itof2IE_batch_bdgs.h"

#include "drchops/Itof2IE_batch.h"


namespace reductionmod
{

  typedef Array1DIterator<npy_double> DblArrIt;
  //typedef Array1DIterator<npy_bool> BoolArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  using DANSE::Reduction::utils::deleteHeapObj;

  namespace Itof2IE_batch_impl {

    template <typename DataIterator, int datatypecode,
	      typename FLT>
    PyObject * call_numpyarray
    (PyObject *pytofbb, PyObject *pycntsmat, PyObject *pyE2mat,
     PyObject *pyebb, 
     PyObject *pyIpixE, PyObject *pyIE2pixE, 
     PyObject *pydistarr, 
     PyObject *pytmpE,
     const FLT & ei, const FLT & mod2sample )
    {
      if (checkDataType(pytofbb, "tofbb", datatypecode)) return 0;
      if (checkDataType(pycntsmat, "cntsmat", datatypecode)) return 0;
      if (checkDataType(pyE2mat, "E2mat", datatypecode)) return 0;
      if (checkDataType(pyebb, "ebb",  datatypecode)) return 0;
      if (checkDataType(pyIpixE, "IpixE", datatypecode)) return 0;
      if (checkDataType(pyIE2pixE, "IE2pixE", datatypecode)) return 0;
      if (checkDataType(pydistarr, "distarr",  datatypecode)) return 0;
      if (checkDataType(pytmpE, "tmpE",  datatypecode)) return 0;
      
      std::ostringstream oss;

      size_t ntofbbs = PyArray_Size( pytofbb ), totsize = PyArray_Size( pycntsmat ),
	totsize1 = PyArray_Size( pyE2mat );
    
      if (totsize != totsize1 || totsize == 0) {
	oss << "Size mismatch: "
	    << "cnts[*,tof] : size = " << totsize << ", "
	    << "errs[*,tof] : size = " << totsize1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      size_t npixels = totsize/(ntofbbs-1);
      if (totsize != npixels * (ntofbbs-1) ) {
	oss << "Invalid shape: "
	    << "ntof * npixels != totsize." << std::endl
	    << ntofbbs-1 << " * " << npixels << " != " << totsize 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t nebbs = PyArray_Size( pyebb ),
	nIpixE = PyArray_Size( pyIpixE ), nIpixE1 = PyArray_Size( pyIE2pixE );

      if (nIpixE != nIpixE1 || nIpixE==0 ) {
	oss << "Size mismatch: "
	    << "I[pix,E] : size = " << nIpixE << ", "
	    << "I_E2[pix,E] : size = " << nIpixE1
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      if (nIpixE != npixels * (nebbs-1) ) {
	oss << "Invalid shape: "
	    << "npixels * ne !=  size(I[pix,E])." << std::endl
	    << npixels << " * " << nebbs-1 << " != " << nIpixE
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t 
	distsize = PyArray_Size( pydistarr )
	;
      if (npixels != distsize || npixels == 0) {
	oss << "Size mismatch: "
	    << "npixels = " << npixels << ","
	    << "distsize = " << distsize << ","
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t tmpEsize = PyArray_Size( pytmpE );
      if (ntofbbs > tmpEsize || tmpEsize == 0) {
	oss << "Size mismatch: "
	    << "tmpE array length " << tmpEsize << " should be larger than "
	    << "the number of tof bin boundaries " << ntofbbs;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      DataIterator tofbb_begin (pytofbb), tofbb_end = tofbb_begin + ntofbbs,
	cntsmat_begin(pycntsmat), E2mat_begin( pyE2mat ),
	ebb_begin( pyebb ), ebb_end = ebb_begin + nebbs,
	IpixE_begin(pyIpixE), IE2pixE_begin(pyIE2pixE),
	dist_begin( pydistarr ),
	tmpE_begin( pytmpE );
      
      //    std::cout << "ei=" << ei<< ", mod2sample =" << mod2sample << std::endl;
      using namespace DANSE::Reduction;
      Itof2IE_batch
	<FLT, DataIterator, DataIterator, DataIterator, DataIterator>
	(tofbb_begin, tofbb_end, 
	 cntsmat_begin, E2mat_begin,
	 ebb_begin, ebb_end,
	 IpixE_begin, IE2pixE_begin,
	 ei, mod2sample,
	 dist_begin,
	 npixels,
	 tmpE_begin
	 );
      
      return Py_None;
    }
    
  }

  char Itof2IE_batch_numpyarray__name__[] = "Itof2IE_batch_numpyarray";
  char Itof2IE_batch_numpyarray__doc__[] = "Itof2IE_batch_numpyarray\n"\
  "Itof2IE_batch( tofbb, cntsmat, E2mat, \n"\
  "               ebb, IpixE, IE2pixE, \n"\
  "               ei, mod2sample, \n"\
  "               distarr, \n"\
  "               tmpE,)\n"\
  "tofbb: tof bin boundaries\n"\
  "cntsmat: counts[*,tof] matrix\n"   \
  "E2mat: error bar square of counts[*,tof] matrix\n"   \
  "ebb: e bin boundaries\n" \
  "IpixE: I[pix,E] matrix \n" \
  "IE2pixE: error bar square of I[phi,E] matrix\n"\
  "ei: incident energy (meV)\n"\
  "mod2sample: moderator-to-sample distance (mm)\n"\
  "distarr: distance[*] array\n"\
  "tmpE: a temporary array. length = len(tofbb) \n"	\
  ;

  PyObject * Itof2IE_batch_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pytofbb, *pycntsmat, *pyE2mat,
      *pyebb, *pyIpixE, *pyIE2pixE,
      *pydistarr,
      *pytmpE;
    npy_double ei, mod2sample;

    int ok = PyArg_ParseTuple
      (args, "OOOOOOddOO", 
       &pytofbb, &pycntsmat, &pyE2mat,
       &pyebb, &pyIpixE, &pyIE2pixE,
       &ei, &mod2sample, 
       &pydistarr,
       &pytmpE
       );

    if (!ok) return 0;

    return Itof2IE_batch_impl::call_numpyarray
      <DblArrIt, NPY_DOUBLE,
      npy_double>
      (pytofbb, pycntsmat, pyE2mat,
       pyebb, pyIpixE, pyIE2pixE,
       pydistarr,
       pytmpE,
       ei, mod2sample);

  }
    
} // reductionmod::



// version
// $Id$

// End of file
