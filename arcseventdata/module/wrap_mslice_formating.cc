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

#include "numpy_support.h"
#include "wrap_mslice_formating.h"
#include "arcseventdata/mslice_formating.h"


namespace wrap_arcseventdata
{
  
  using namespace reductionmod;
  using namespace ARCS_EventData;
  
  typedef Array1DIterator<npy_double> DblArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  
  namespace mslice_formating_impl {
    
    template <typename DataType, int TypeCode>
    PyObject * SGrid_str_numpyarray
    (PyObject *pySarray, PyObject *pySEarray,
     size_t npixels, size_t nEbins)
    {
      if (checkDataType(pySarray, "Sarray", TypeCode)) return 0;
      if (checkDataType(pySEarray, "SEarray", TypeCode)) return 0;

      std::ostringstream oss;

      size_t nSarrsize = PyArray_Size( pySarray );
      size_t nSEarrsize = PyArray_Size( pySEarray );
      
      if (nSEarrsize != nSarrsize or nSarrsize != (npixels*nEbins)) {
	oss << "Size mismatch: "
	    << "Sarray: size = " << nSarrsize << "; "
	    << "SEarray: size = " << nSEarrsize << "; "
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      typedef Array1DIterator<DataType> Iterator;
      Iterator S_begin(pySarray);
      Iterator SE_begin(pySEarray);
      
      const char * s = SGrid_str
	(S_begin, SE_begin, npixels, nEbins);
      
      return Py_BuildValue( "s", s );
    }
    
  }
 
  
  // 
  char SGrid_str_numpyarray__name__[] = "SGrid_str_numpyarray";
  char SGrid_str_numpyarray__doc__[] = "SGrid_str_numpyarray\n" \
"SGrid_str( S_arr, SE_arr, npixels, nEbins)"
;
  // S_arr: numpy array of S(pix,E)
  // SE_arr: numpy array of S_error(pix,E)
  // npixels: number of pixels
  // nEbins: number of E bins
  
  PyObject * SGrid_str_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pySarr, *pySEarr;
    long npixels, nEbins;
    
    int ok = PyArg_ParseTuple
      (args, "OOll", 
       &pySarr, &pySEarr, 
       &npixels, &nEbins);
    
    if (!ok) return 0;

    return mslice_formating_impl::SGrid_str_numpyarray
      <npy_double, NPY_DOUBLE>
      (pySarr, pySEarr, npixels, nEbins);
      ;
  }
  

} // wrap_arcseventdata::



// version
// $Id$

// End of file
