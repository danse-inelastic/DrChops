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
#include "wrap_normalize_iqqqe.h"

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_iqqqe.h"



namespace wrap_arcseventdata
{
  
  using namespace reductionmod;
  using namespace ARCS_EventData;
  
  typedef Array1DIterator<npy_double> DblArrIt;

  
  namespace normalize_iqqqe_impl {
    
    PyObject * call_calcSolidAngleQQQE
    ( double qxbegin, double qxend, double qxstep,
      double qybegin, double qyend, double qystep,
      double qzbegin, double qzend, double qzstep,
      double ebegin, double eend, double estep,
      PyObject *pySAarray,
      double ei, 
      unsigned int npixels, 
      const double *pixelPositions, const double *pixelsolidangles,
      const AbstractMask *mask)
    {
      if (checkDataType(pySAarray, "saarray", NPY_DOUBLE)) return 0;

      size_t nSAarrsize = PyArray_Size( pySAarray );
      size_t nqx = (qxend-qxbegin)/qxstep, nqy = (qyend-qybegin)/qystep, nqz = (qzend-qzbegin)/qzstep;
      size_t ne = (eend-ebegin)/estep;

      if (nSAarrsize != nqx*nqy*nqz*ne ) {
	std::ostringstream oss;
	oss << "Size mismatch: "
	    << "SAarray: size = " << nSAarrsize << "; "
	    << "qx bin boundaries parameters = " << qxbegin << ", " << qxend << ", " << qxstep
	    << "qy bin boundaries parameters = " << qybegin << ", " << qyend << ", " << qystep
	    << "qz bin boundaries parameters = " << qzbegin << ", " << qzend << ", " << qzstep
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
      
      typedef EvenlySpacedGridData_4D< double, double, double, double, double, Iterator> IQQQE;

      IQQQE sa
	( qxbegin, qxend, qxstep,
	  qybegin, qyend, qystep,
	  qzbegin, qzend, qzstep,
	  ebegin, eend, estep,
	  sa_begin );

      calcSolidAngleQQQE
	<IQQQE, double, unsigned int>
	( sa, ei, 
	  npixels, pixelPositions,  pixelsolidangles,
	  *mask);
      
      return Py_None;
    }
    
  }
 
  
  // 
  char calcSolidAngleQQQE_numpyarray__name__[] = "calcSolidAngleQQQE_numpyarray";
  char calcSolidAngleQQQE_numpyarray__doc__[] = "calcSolidAngleQQQE_numpyarray\n" \
"calcSolidAngleQQQE( qxbegin, qxend, qxstep, qybegin, qyend, qystep, qzbegin, qzend, qzstep,"
"                    ebegin, eend, estep, SAnpyarr, "\
"               ei, npixels, pixelPositions, pixelsolidangles, mask)"
;
  // {qibegin, qiend, qistep} i=x,y,z,  and  ebegin, eend, estep, SAnpyarr defines a "histogram"
  // ei: incident energy
  // npixels: total number of pixels
  // pixelPositions: double array of pixel positions
  // pixelsolidangles: double array of pixel solid angles
  // mask: detector mask (optional)
  //
  PyObject * calcSolidAngleQQQE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pySAnpyarr, *pypixelPositions, *pypixelsolidangles, *pymask = NULL;
    double qxbegin, qxend, qxstep;
    double qybegin, qyend, qystep;
    double qzbegin, qzend, qzstep;
    double ebegin, eend, estep;
    double ei;
    long npixels;
    
    int ok = PyArg_ParseTuple
      (args, "ddddddddddddOdlOO|O", 
       &qxbegin, &qxend, &qxstep, 
       &qybegin, &qyend, &qystep, 
       &qzbegin, &qzend, &qzstep, 
       &ebegin, &eend, &estep, &pySAnpyarr, 
       &ei, &npixels, &pypixelPositions, &pypixelsolidangles,
       &pymask);
    
    if (!ok) return 0;

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

    // call
    PyObject * ret =  normalize_iqqqe_impl::call_calcSolidAngleQQQE
      (qxbegin, qxend, qxstep, 
       qybegin, qyend, qystep, 
       qzbegin, qzend, qzstep, 
       ebegin, eend, estep, pySAnpyarr, 
       ei, npixels, pixelPositions, pixelsolidangles, mask);

    if (pymask == NULL) {
      delete mask;
    }

    return ret;
  }
  

} // wrap_arcseventdata5A::



// version
// $Id$

// End of file
