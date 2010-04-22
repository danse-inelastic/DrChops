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
#include "wrap_normalize_iqe.h"

#include "arcseventdata/AbstractMask.h"
#include "arcseventdata/normalize_iqe.h"



namespace wrap_arcseventdata
{
  
  using namespace reductionmod;
  using namespace ARCS_EventData;
  
  typedef Array1DIterator<npy_double> DblArrIt;

  
  namespace normalize_iqe_impl {
    
    PyObject * call_calcSolidAngleQE
    ( double qbegin, double qend, double qstep,
      double ebegin, double eend, double estep,
      PyObject *pySAarray,
      double ei, 
      unsigned int npixels, 
      const double *pixelPositions, const double *pixelsolidangles,
      const AbstractMask *mask)
    {
      if (checkDataType(pySAarray, "saarray", NPY_DOUBLE)) return 0;

      size_t nSAarrsize = PyArray_Size( pySAarray );
      
      if (nSAarrsize != size_t( (qend-qbegin)/qstep) * size_t((eend-ebegin)/estep ) ) {
	std::ostringstream oss;
	oss << "Size mismatch: "
	    << "SAarray: size = " << nSAarrsize << "; "
	    << "q bin boundaries parameters = " << qbegin << ", " << qend << ", " << qstep << "; "
	    << "e bin boundaries parameters = " << ebegin << ", " << eend << ", " << estep << "; "
	    << "qsize=" << size_t( (qend-qbegin)/qstep) << "; "
	    << "esize=" << size_t( (eend-ebegin)/estep) << "; "
	    << std::endl;
	oss << "This could be caused by python floating-point-number error."
	    << "You can try to change the step size and see if that helps."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      typedef Array1DIterator<double> Iterator;
      Iterator sa_begin(pySAarray);
      
      typedef EvenlySpacedGridData_2D< double, double, double, Iterator> IQE;

      IQE sa( qbegin, qend, qstep,
	      ebegin, eend, estep,
	      sa_begin );

      calcSolidAngleQE
	<IQE, double, unsigned int>
	( sa, ei, 
	  npixels, pixelPositions, pixelsolidangles,
	  *mask);
      
      return Py_None;
    }
    
  }
 
  
  // 
  char calcSolidAngleQE_numpyarray__name__[] = "calcSolidAngleQE_numpyarray";
  char calcSolidAngleQE_numpyarray__doc__[] = "calcSolidAngleQE_numpyarray\n" \
"calcSolidAngleQE( qbegin, qend, qstep, ebegin, eend, estep, SAnpyarr, "\
"               ei, npixels, pixelPositions, pixelsolidangles, mask)"
;
  // qbegin, qend, qstep, ebegin, eend, estep, SAnpyarr defines a "histogram"
  // ei: incident energy
  // npixels: total number of pixels
  // pixelPositions: double array of pixel positions
  // pixelsolidangles: double array of pixel solid angles
  // mask: detector mask (optional)
  //
  PyObject * calcSolidAngleQE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pySAnpyarr, *pypixelPositions, *pypixelsolidangles, *pymask = NULL;
    double qbegin, qend, qstep, ebegin, eend, estep;
    double ei;
    long npixels;
    
    int ok = PyArg_ParseTuple
      (args, "ddddddOdlO|O", 
       &qbegin, &qend, &qstep, &ebegin, &eend, &estep, &pySAnpyarr, 
       &ei,&npixels, &pypixelPositions, &pypixelsolidangles, &pymask);
    
    if (!ok) return 0;

    // pixelPositions
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

    // pixelsolidangles
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
    PyObject * ret =  normalize_iqe_impl::call_calcSolidAngleQE(
      qbegin, qend, qstep, ebegin, eend, estep, pySAnpyarr, 
      ei,npixels, pixelPositions, pixelsolidangles, mask);

    if (pymask == NULL) {
      delete mask;
    }

    return ret;
  }
  

} // wrap_arcseventdata5A::



// version
// $Id$

// End of file
