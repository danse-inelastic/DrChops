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
#include "wrap_normalize_ihkle.h"

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_ihkle.h"



namespace wrap_arcseventdata
{
  
  using namespace reductionmod;
  using namespace ARCS_EventData;
  
  typedef Array1DIterator<npy_double> DblArrIt;

  
  namespace normalize_ihkle_impl {
    
    PyObject * call_calcSolidAngleHKLE
    ( double hbegin, double hend, double hstep,
      double kbegin, double kend, double kstep,
      double lbegin, double lend, double lstep,
      double ebegin, double eend, double estep,
      PyObject *pySAarray,
      double ei, double *ub_store,
      unsigned int npixels, 
      const double *pixelPositions, const double *pixelsolidangles,
      const AbstractMask *mask)
    {
      if (checkDataType(pySAarray, "saarray", NPY_DOUBLE)) return 0;

      size_t nSAarrsize = PyArray_Size( pySAarray );
      size_t nh = (hend-hbegin)/hstep, nk = (kend-kbegin)/kstep, nl = (lend-lbegin)/lstep;
      size_t ne = (eend-ebegin)/estep;

      if (nSAarrsize != nh*nk*nl*ne ) {
	std::ostringstream oss;
	oss << "Size mismatch: "
	    << "SAarray: size = " << nSAarrsize << "; "
	    << "h bin boundaries parameters = " << hbegin << ", " << hend << ", " << hstep
	    << "k bin boundaries parameters = " << kbegin << ", " << kend << ", " << kstep
	    << "l bin boundaries parameters = " << lbegin << ", " << lend << ", " << lstep
	    << "e bin boundaries parameters = " << ebegin << ", " << eend << ", " << estep
	    << std::endl;
	oss << "This could be caused by python floating-point-number error."
	    << "You can try to change the step size and see if that helps."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      typedef Array1DIterator<double> Iterator;
      Iterator sa_begin(pySAarray);
      
      typedef EvenlySpacedGridData_4D< double, double, double, double, double, Iterator> IHKLE;

      IHKLE sa
	( hbegin, hend, hstep,
	  kbegin, kend, kstep,
	  lbegin, lend, lstep,
	  ebegin, eend, estep,
	  sa_begin );

      double *ub[3];
      for (int i=0; i<3; i++) ub[i] = ub_store+3*i;
      
      calcSolidAngleHKLE
	<IHKLE, double, unsigned int>
	( sa, ei, ub,
	  npixels, pixelPositions, pixelsolidangles,
	  *mask);
      
      return Py_None;
    }
    
  }
 
  
  // 
  char calcSolidAngleHKLE_numpyarray__name__[] = "calcSolidAngleHKLE_numpyarray";
  char calcSolidAngleHKLE_numpyarray__doc__[] = "calcSolidAngleHKLE_numpyarray\n" \
"calcSolidAngleHKLE( hbegin, hend, hstep, kbegin, kend, kstep, lbegin, lend, lstep,"
"                    ebegin, eend, estep, SAnpyarr, "\
"               ei, ub, npixels, pixelPositions, pixelsolidangles, mask)"
;
  // {qbegin, qend, qstep} q=h,k,l  and  ebegin, eend, estep, SAnpyarr defines a "histogram"
  // ei: incident energy
  // ub: matrix to convert Q vector to hkl
  // npixels: total number of pixels
  // pixelPositions: double array of pixel positions
  // pixelsolidangles: double array of pixel solid angles
  // mask: detector mask (optional)
  //
  PyObject * calcSolidAngleHKLE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pySAnpyarr, *pypixelPositions, *pypixelsolidangles, 
      *pymask = NULL;
    double hbegin, hend, hstep;
    double kbegin, kend, kstep;
    double lbegin, lend, lstep;
    double ebegin, eend, estep;
    double ei;
    PyObject *pyub;
    long npixels;
    
    int ok = PyArg_ParseTuple
      (args, "ddddddddddddOdOlOO|O", 
       &hbegin, &hend, &hstep, 
       &kbegin, &kend, &kstep, 
       &lbegin, &lend, &lstep, 
       &ebegin, &eend, &estep, &pySAnpyarr, 
       &ei, &pyub, &npixels, &pypixelPositions, &pypixelsolidangles,
       &pymask);
    
    if (!ok) return 0;

    // convert ub from python object to a double array
    if (!PyTuple_Check(pyub) || PyTuple_Size(pyub)!=3 ) {
      PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple");
      return 0;
    }
    double ub[9];
    for (int i=0; i<3; i++) {
      PyObject *item = PyTuple_GetItem(pyub, i);

      if (!PyTuple_Check(item) || PyTuple_Size(item)!=3) {
	PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple of 3-tuples");
	return 0;
      }
      for (int j=0; j<3; j++) {
	PyObject *pynum = PyTuple_GetItem(item,j);
	if (!PyFloat_Check(pynum)) {
	  PyErr_SetString( PyExc_ValueError, "ub matrix must be a 3-tuple of 3-tuples of floats");
	  return 0;
	}
	ub[3*i+j] = PyFloat_AsDouble(pynum);
      }
    }


    // pixel positions
    if (pypixelPositions == NULL) {
	std::ostringstream oss;
	oss << "The PyCObject for pixelPositions is a null pointer.";
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
    }

    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );

    if (pixelPositions == NULL ) {
	std::ostringstream oss;
	oss << "The pixelPositions pointer is a null pointer.";
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
    }

    // pixel solid angles
    if (pypixelsolidangles == NULL) {
	std::ostringstream oss;
	oss << "The PyCObject for pixelsolidangles is a null pointer.";
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
    }

    const double * pixelsolidangles = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelsolidangles ) );

    if (pixelsolidangles == NULL ) {
	std::ostringstream oss;
	oss << "The pixelsolidangles pointer is a null pointer.";
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
    }

    // mask
    AbstractMask * mask;
    if (pymask != NULL) {
      mask = static_cast< AbstractMask * >
	(PyCObject_AsVoidPtr( pymask ) );
      if (mask == NULL) {
	std::ostringstream oss;
	oss << "The mask pointer is a null pointer.";
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
    }
    else {
      mask = new NoMask;
    }

    PyObject * ret =  normalize_ihkle_impl::call_calcSolidAngleHKLE
      (hbegin, hend, hstep, 
       kbegin, kend, kstep, 
       lbegin, lend, lstep, 
       ebegin, eend, estep, pySAnpyarr, 
       ei, ub, npixels, pixelPositions, pixelsolidangles, mask);

    if (pymask == NULL) {
      delete mask;
    }

    return ret;
  }
  

} // wrap_arcseventdata5A::



// version
// $Id$

// End of file
