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

#include "utils.h"
#include "numpy_support.h"
#include "IpixE2IphiE_bdgs.h"

#include "drchops/IpixE2IphiE.h"


namespace reductionmod
{

  typedef Array1DIterator<npy_double> DblArrIt;
  //typedef Array1DIterator<npy_bool> BoolArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  using DANSE::Reduction::utils::deleteHeapObj;

  namespace IpixE2IphiE_impl {

    template <typename DataIterator, int datatypecode,
	      typename MaskIterator, int masktypecode,
	      typename FLT>
    PyObject * call_numpyarray
    (PyObject *pyebb, PyObject *pyIpixE, PyObject *pyE2pixE,
     PyObject *pyoutphibb, 
     PyObject *pyIphiE, PyObject *pyE2phiE, 
     PyObject *pysaphi, PyObject *pysaE2phi,
     PyObject *pyphiarr, 
     PyObject *pysaarr, PyObject *pysaE2arr,
     PyObject *pymaskarr
     )

    {
      if (checkDataType(pyebb, "ebb", datatypecode)) return 0;
      if (checkDataType(pyIpixE, "IpixE", datatypecode)) return 0;
      if (checkDataType(pyE2pixE, "E2pixE", datatypecode)) return 0;
      if (checkDataType(pyoutphibb, "outphibb",  datatypecode)) return 0;
      if (checkDataType(pyIphiE, "IphiE",  datatypecode)) return 0;
      if (checkDataType(pyE2phiE, "E2phiE",  datatypecode)) return 0;
      if (checkDataType(pysaphi, "solidangle[phi]",  datatypecode)) return 0;
      if (checkDataType(pysaE2arr, "solidangleE2[phi]",  datatypecode)) return 0;
      if (checkDataType(pyphiarr, "phiarr",  datatypecode)) return 0;
      if (checkDataType(pysaarr, "saarr",  datatypecode)) return 0;
      if (checkDataType(pysaE2arr, "saE2arr",  datatypecode)) return 0;
      if (checkDataType(pymaskarr, "maskarr",  masktypecode)) return 0;
      
      std::ostringstream oss;

      size_t nebbs = PyArray_Size( pyebb ), IpixESize = PyArray_Size( pyIpixE ),
	IpixESize1 = PyArray_Size( pyE2pixE );
    
      if (IpixESize != IpixESize1 || IpixESize == 0) {
	oss << "Size mismatch: "
	    << "cnts[*,E] : size = " << IpixESize << ", "
	    << "errs[*,E] : size = " << IpixESize1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      size_t npixels = IpixESize/(nebbs-1);
      if (IpixESize != npixels * (nebbs-1) ) {
	oss << "Invalid shape: "
	    << "nE * npixels != IpixESize." << std::endl
	    << nebbs-1 << " * " << npixels << " != " << IpixESize 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t nphibbs = PyArray_Size( pyoutphibb ), 
	IphiESize = PyArray_Size( pyIphiE ), IphiESize1 = PyArray_Size( pyE2phiE );

      if (IphiESize != IphiESize1 || IphiESize==0 ) {
	oss << "Size mismatch: "
	    << "I[phi,E] : size = " << IphiESize << ", "
	    << "I_err2[phi,E] : size = " << IphiESize1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      if (IphiESize != (nphibbs-1) * (nebbs-1) ) {
	oss << "Invalid shape: "
	    << "nphi * ne !=  size(S)." << std::endl
	    << nphibbs-1 << " * " << nebbs-1 << " != " << IphiESize 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t masksize = PyArray_Size( pymaskarr ), 
	phisize = PyArray_Size( pyphiarr ),
	sasize = PyArray_Size( pysaarr ),
	saE2size = PyArray_Size( pysaE2arr )
	;
      if (npixels != masksize || npixels != phisize 
	  || npixels!=sasize || npixels != saE2size 
	  || npixels == 0) {
	oss << "Size mismatch: "
	    << "npixels = " << npixels << ","
	    << "masksize = " << masksize << ","
	    << "phisize = " << phisize << ","
	    << "sasize = " << sasize << ","
	    << "saE2size = " << saE2size << ","
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      DataIterator ebb_begin (pyebb), ebb_end = ebb_begin + nebbs,
	IpixE_begin(pyIpixE), E2pixE_begin( pyE2pixE ),
	outphibb_begin( pyoutphibb ), outphibb_end = outphibb_begin + nphibbs,
	IphiE_begin(pyIphiE), E2phiE_begin( pyE2phiE ), 
	saphi_begin(pysaphi), saE2phi_begin(pysaE2phi), 
	phi_begin( pyphiarr ), 
	sa_begin( pysaarr ), saE2_begin( pysaE2arr )
	;
      
      MaskIterator mask_begin( pymaskarr );

      //    std::cout << "ei=" << ei<< ", mod2sample =" << mod2sample << std::endl;
      using namespace DANSE::Reduction;
      IpixE2IphiE
	<FLT, DataIterator, DataIterator, DataIterator, DataIterator, MaskIterator>
	(ebb_begin, ebb_end, 
	 IpixE_begin, E2pixE_begin,
	 outphibb_begin, outphibb_end,
	 IphiE_begin, E2phiE_begin,
	 saphi_begin, saE2phi_begin,

	 phi_begin, 
	 sa_begin,
	 saE2_begin,
	 mask_begin, 
	 npixels
	 );
      
      return Py_None;
    }
    
  }

  // constructor
  char IpixE2IphiE_numpyarray__name__[] = "IpixE2IphiE_numpyarray";
  char IpixE2IphiE_numpyarray__doc__[] = "IpixE2IphiE_numpyarray\n"\
  "IpixE2IphiE( Ebb, IpixE, E2pixE, \n"\
  "             outphibb, IphiE, E2phiE, saphi, saE2phi\n"\
  "             phiarr, saarr, saE2arr, maskarr) \n"\
  "ebb: e bin boundaries\n" \
  "IpixE: counts[*,tof] matrix\n"   \
  "E2pixE: counts_err2[*,tof] matrix\n"   \
  "outphibb: phi bin boundaries for the output I[phi,E]\n" \
  "IphiE: I[phi,E] matrix \n" \
  "E2phiE: error bar square of I[phi,E] matrix\n"\
  "saphi: solid angle[phi] \n" \
  "saE2phi: error bar square of solid angle[phi]\n"\
  "phiarr: phi[*] array\n"\
  "saarr: solidangle[*] array\n"\
  "saE2arr: error bar square of solidangle[*] array\n"\
  "maskarr: mask[*] array\n"\
  ;

  PyObject * IpixE2IphiE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyebb, *pyIpixE, *pyE2pixE,
      *pyoutphibb, *pyIphiE, *pyE2phiE, *pysaphi, *pysaE2phi,
      *pyphiarr, *pysaarr, *pysaE2arr, *pymaskarr
      ;

    int ok = PyArg_ParseTuple
      (args, "OOOOOOOOOOOO", 
       &pyebb, &pyIpixE, &pyE2pixE,
       &pyoutphibb, &pyIphiE, &pyE2phiE, &pysaphi, &pysaE2phi,
       &pyphiarr, &pysaarr, &pysaE2arr, &pymaskarr
       );

    if (!ok) return 0;

    return IpixE2IphiE_impl::call_numpyarray
      <DblArrIt, NPY_DOUBLE,
      IntArrIt, NPY_INT,
      npy_double>
      (pyebb, pyIpixE, pyE2pixE,
       pyoutphibb, pyIphiE, pyE2phiE, pysaphi, pysaE2phi,
       pyphiarr, pysaarr, pysaE2arr, pymaskarr
       );

  }
    
} // reductionmod::



// version
// $Id: IpixE2IphiE_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
