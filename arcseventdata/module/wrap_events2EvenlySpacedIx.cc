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
#include "wrap_events2EvenlySpacedIx.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIx.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/Event2d.h"
#include "arcseventdata/Event2tof.h"


namespace wrap_arcseventdata
{
  
  using namespace reductionmod;
  using namespace ARCS_EventData;
  
  typedef Array1DIterator<npy_double> DblArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  
  namespace events2EvenlySpacedIx_impl {
    
    template <typename Event2X, 
	      typename XData,
	      typename YData, int YTypeCode
	      >
    PyObject * call_numpyarray
    (const Event2X & e2x,
     PyObject * pyevents, size_t N,
     XData x_begin, XData x_end, XData x_step, 
     PyObject *pyyarray)
    {
      if (checkDataType(pyyarray, "yarray", YTypeCode)) return 0;

      std::ostringstream oss;

      const Event *events_begin = (const Event *)PyCObject_AsVoidPtr( pyevents );
      //std::cout << "events_begin = " << events_begin << std::endl;
      if (events_begin == 0) {
	oss << "first argument must be a PyCObject of a void pointer " 
	    << "pointing to an events array."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      //std::cout << "hello" << std::endl;
      size_t nyarrsize = PyArray_Size( pyyarray );
      
      //std::cout << "hello" << std::endl;
      //std::cout << x_begin << ", " << x_end << ", " << x_step << std::endl;
      if (nyarrsize != size_t( (x_end-x_begin)/x_step) ) {
	oss << "Size mismatch: "
	    << "yarray: size = " << nyarrsize << "; "
	    << "expected size (end-begin)/step = " << size_t((x_end-x_begin)/x_step) << ";"
	    << "x bin boundaries parameters = " << x_begin << ", " << x_end << ", " << x_step
	    << std::endl;
	oss << "This could be caused by python floating-point-number error."
	    << "You can try to change the step size and see if that helps."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      //std::cout << "hello" << std::endl;
      
      typedef Array1DIterator<YData> YIterator;
      YIterator y_begin(pyyarray);
      
      events2EvenlySpacedIx<Event2X, XData, YData>
	(events_begin, N, e2x, x_begin, x_end, x_step, y_begin);

      return Py_None;
    }
    
  }
 
  
  // 
  char events2Ipix_numpyarray__name__[] = "events2Ipix_numpyarray";
  char events2Ipix_numpyarray__doc__[] = "events2Ipix_numpyarray\n" \
"events2Ipix( events, N, pixbegin, pixend, pixstep, intensities )"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // pixbegin, pixend, pixstep: integers.
  // intensities: numpy array to store I(pix)
  
  PyObject * events2Ipix_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    int pixbegin, pixend, pixstep;
    
    int ok = PyArg_ParseTuple
      (args, "OliiiO", 
       &pyevents, &N, 
       &pixbegin, &pixend, &pixstep,
       &pyintensities);
    
    if (!ok) return 0;

    return events2EvenlySpacedIx_impl::call_numpyarray
      <Event2pixelID, 
      unsigned int, npy_int, NPY_INT>
      (e2pixelID,
       pyevents, N,
       pixbegin, pixend, pixstep, 
       pyintensities)
      ;
  }
  

  // 
  char events2Itof_numpyarray__name__[] = "events2Itof_numpyarray";
  char events2Itof_numpyarray__doc__[] = "events2Itof_numpyarray\n" \
"events2Itof( events, N, tofbegin, tofend, tofstep, intensities, "
"             ntotpixels=(115+1)*8*128, tofUnit=1.e-7 )"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // tofbegin, tofend, tofstep: floats to define tof axis.
  // intensities: numpy array to store I(tof)
  // ntotpixels: total # of pixels
  // tofUnit: tof unit
  
  PyObject * events2Itof_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double tofbegin, tofend, tofstep;
    long ntotpixels = (1+115)*8*128; double tofUnit = 1e-7;
    
    int ok = PyArg_ParseTuple
      (args, "OldddO|ld", 
       &pyevents, &N, 
       &tofbegin, &tofend, &tofstep,
       &pyintensities, 
       &ntotpixels, &tofUnit);
    
    if (!ok) return 0;

    Event2tof e2t( ntotpixels, tofUnit );
    return events2EvenlySpacedIx_impl::call_numpyarray
      <Event2tof, 
      double, npy_int, NPY_INT>
      (e2t,
       pyevents, N,
       tofbegin, tofend, tofstep, 
       pyintensities)
      ;
  }
  

  // 
  char events2Idspacing_numpyarray__name__[] = "events2Idspacing_numpyarray";
  char events2Idspacing_numpyarray__doc__[] = "events2Idspacing_numpyarray\n" \
"events2Idspacing( events, N, dbegin, dend, dstep, intensities, pixelPositions, ntotpixels, tofUnit, mod2sample )"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // dbegin, dend, dstep: dspacing axis parameters
  // intensities: numpy array to store I(d)
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  
  PyObject * events2Idspacing_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double dbegin, dend, dstep;
    PyObject *pypixelPositions;
    long ntotpixels=  (1+115)*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    
    int ok = PyArg_ParseTuple
      (args, "OldddOO|ldd", 
       &pyevents, &N, 
       &dbegin, &dend, &dstep,
       &pyintensities,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2d e2d( pixelPositions, ntotpixels, tofUnit, mod2sample );
    
    return events2EvenlySpacedIx_impl::call_numpyarray
      <Event2d,
      double, npy_int, NPY_INT>
      (e2d,
       pyevents, N,
       dbegin, dend, dstep, 
       pyintensities)
      ;
  }
  


} // wrap_events2EvenlySpacedIx::



// version
// $Id$

// End of file
