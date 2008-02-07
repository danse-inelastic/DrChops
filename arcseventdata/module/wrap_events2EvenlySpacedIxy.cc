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
#include "wrap_events2EvenlySpacedIxy.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIxy.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/Event2pixE.h"
#include "arcseventdata/Event2QE.h"
#include "arcseventdata/Event2pixtof.h"
#include "arcseventdata/Event2pixd.h"

#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace wrap_arcseventdata
{

  namespace wrap_events2EvenlySpacedIxy_Impl {
    const char jrnltag[] = "events2EvenlySpacedIxy";
  }
  
  using namespace ARCS_EventData;
  using namespace reductionmod;
  
  typedef Array1DIterator<npy_double> DblArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  
  namespace events2EvenlySpacedIxy_impl {
    
    template <typename Event2XY, 
	      typename XData, typename YData,
	      typename ZData, int ZTypeCode
	      >
    PyObject * call_numpyarray
    (const Event2XY & e2xy,
     PyObject * pyevents, size_t N,
     XData x_begin, XData x_end, XData x_step, 
     YData y_begin, YData y_end, YData y_step, 
     PyObject *pyzarray)
    {
      if (checkDataType(pyzarray, "zarray", ZTypeCode)) return 0;

      std::ostringstream oss;

      const Event *events_begin = (const Event *)
	PyCObject_AsVoidPtr( pyevents );
#ifdef DEBUG
      journal::debug_t debug( wrap_events2EvenlySpacedIxy_Impl::jrnltag );
      debug << journal::at(__HERE__)
	    << "events_begin = " << events_begin 
	    << journal::endl;
#endif
      if (events_begin == 0) {
	oss << "first argument must be a PyCObject of a void pointer " 
	    << "pointing to an events array."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      //std::cout << "hello" << std::endl;
      size_t nzarrsize = PyArray_Size( pyzarray );
      
      //std::cout << "hello" << std::endl;
      //std::cout << x_begin << ", " << x_end << ", " << x_step << std::endl;
      if (nzarrsize != size_t( (x_end-x_begin)/x_step) * size_t( (y_end-y_begin)/y_step) )  {
	oss << "Size mismatch: "
	    << "zarray: size = " << nzarrsize << "; "
	    << "x bin boundaries parameters = " << x_begin << ", " << x_end << ", " << x_step
	    << "y bin boundaries parameters = " << y_begin << ", " << y_end << ", " << y_step
	    << std::endl;
	oss << "This could be caused by python floating-point-number error."
	    << "You can try to change the step size and see if that helps."
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      //std::cout << "hello" << std::endl;
      
      typedef Array1DIterator<ZData> ZIterator;
      ZIterator z_begin(pyzarray);
      
      events2EvenlySpacedIxy<Event2XY, XData, YData, ZData, ZIterator>
	(events_begin, N, e2xy, 
	 x_begin, x_end, x_step, 
	 y_begin, y_end, y_step, 
	 z_begin);

      return Py_None;
    }
    
  }
 
  
  // 
  char events2IpixE_numpyarray__name__[] = "events2IpixE_numpyarray";
  char events2IpixE_numpyarray__doc__[] = "events2IpixE_numpyarray\n" \
"events2IpixE( events, N, pixel_begin, pixel_end, pixel_step, \n"\
"                E_begin, E_end, E_step, \n"\
"                intensities, Ei, pixelPositions, ntotpixels, tofUnit, mod2sample)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // pixel_begin, pixel_end, pixel_step: pixel axis parameters
  // E_begin, E_end, E_step: E axis parameters
  // intensities: numpy array to store I(d)
  // Ei: incident neutron energy
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  // toffset: emission time offset. unit: microsecond
  
  PyObject * events2IpixE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    int pixel_begin, pixel_end, pixel_step;
    double E_begin, E_end, E_step;
    double Ei;
    PyObject *pypixelPositions;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    double toffset = 0;
    
    int ok = PyArg_ParseTuple
      (args, "OliiidddOdO|lddd", 
       &pyevents, &N, 
       &pixel_begin, &pixel_end, &pixel_step,
       &E_begin, &E_end, &E_step,
       &pyintensities,
       &Ei,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample,
       &toffset);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2pixE e2pixE( Ei, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset );
    /*
    std::cout << "pixel axis" 
	      << pixel_begin << ", "
	      << pixel_end << ", "
	      << pixel_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << E_begin << ", "
	      << E_end << ", "
	      << E_step << ", "
	      << std::endl;
    */
    return events2EvenlySpacedIxy_impl::call_numpyarray
      <Event2pixE,
      unsigned int, double, npy_int, NPY_INT>
      (e2pixE,
       pyevents, N,
       pixel_begin, pixel_end, pixel_step, 
       E_begin, E_end, E_step, 
       pyintensities)
      ;
  }
  


  // 
  char events2IQE_numpyarray__name__[] = "events2IQE_numpyarray";
  char events2IQE_numpyarray__doc__[] = "events2IQE_numpyarray\n" \
"events2IQE( events, N, Q_begin, Q_end, Q_step, \n"\
"            E_begin, E_end, E_step, \n"\
"            intensities, Ei, pixelPositions, ntotpixels, tofUnit, \n"\
"            mod2sample, toffset)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // Q_begin, Q_end, Q_step: pixel axis parameters
  // E_begin, E_end, E_step: E axis parameters
  // intensities: numpy array to store I(d)
  // Ei: incident neutron energy
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  // toffset: shutter time offset. unit: microsecond
  
  PyObject * events2IQE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double Q_begin, Q_end, Q_step;
    double E_begin, E_end, E_step;
    double Ei;
    PyObject *pypixelPositions;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    double toffset = 0;
    
    int ok = PyArg_ParseTuple
      (args, "OlddddddOdO|lddd", 
       &pyevents, &N, 
       &Q_begin, &Q_end, &Q_step,
       &E_begin, &E_end, &E_step,
       &pyintensities,
       &Ei,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample,
       &toffset);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2QE e2QE( Ei, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset );
    /*
    std::cout << "pixel axis" 
	      << Q_begin << ", "
	      << Q_end << ", "
	      << Q_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << E_begin << ", "
	      << E_end << ", "
	      << E_step << ", "
	      << std::endl;
    */
    return events2EvenlySpacedIxy_impl::call_numpyarray
      <Event2QE,
      double, double, npy_int, NPY_INT>
      (e2QE,
       pyevents, N,
       Q_begin, Q_end, Q_step, 
       E_begin, E_end, E_step, 
       pyintensities)
      ;
  }
  


  // 
  char events2Ipixtof_numpyarray__name__[] = "events2Ipixtof_numpyarray";
  char events2Ipixtof_numpyarray__doc__[] = "events2Ipixtof_numpyarray\n" \
"events2Ipixtof( events, N, pixel_begin, pixel_end, pixel_step, \n"\
"                tof_begin, tof_end, tof_step, \n"\
"                intensities, ntotpixels, tofUnit)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // pixel_begin, pixel_end, pixel_step: pixel axis parameters
  // tof_begin, tof_end, tof_step: E axis parameters
  // intensities: numpy array to store I(d)
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  
  PyObject * events2Ipixtof_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    int pixel_begin, pixel_end, pixel_step;
    double tof_begin, tof_end, tof_step;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7;
    
    int ok = PyArg_ParseTuple
      (args, "OliiidddO|ld", 
       &pyevents, &N, 
       &pixel_begin, &pixel_end, &pixel_step,
       &tof_begin, &tof_end, &tof_step,
       &pyintensities,
       &ntotpixels, &tofUnit);
    
    if (!ok) return 0;
    
    Event2pixtof e2pixtof( ntotpixels, tofUnit );
    /*
    std::cout << "pixel axis" 
	      << pixel_begin << ", "
	      << pixel_end << ", "
	      << pixel_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << tof_begin << ", "
	      << tof_end << ", "
	      << tof_step << ", "
	      << std::endl;
    */
    return events2EvenlySpacedIxy_impl::call_numpyarray
      <Event2pixtof,
      unsigned int, double, npy_int, NPY_INT>
      (e2pixtof,
       pyevents, N,
       pixel_begin, pixel_end, pixel_step, 
       tof_begin, tof_end, tof_step, 
       pyintensities)
      ;
  }
  

  // 
  char events2Ipixd_numpyarray__name__[] = "events2Ipixd_numpyarray";
  char events2Ipixd_numpyarray__doc__[] = "events2Ipixd_numpyarray\n" \
"events2Ipixd( events, N, pixel_begin, pixel_end, pixel_step, \n"\
"              d_begin, d_end, d_step, \n"\
"              intensities, pixelPositions, ntotpixels, tofUnit, \n"\
"              mod2sample, emission_time)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // pixel_begin, pixel_end, pixel_step: pixel axis parameters
  // d_begin, d_end, d_step: E axis parameters
  // intensities: numpy array to store I(d)
  // pixelPositions: PyCObject of pixel positions array
  // ntotpixels: number of total pixels. actually npack*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator-sampel distance (meter)
  // emission_time: emssion time (microsecond)
  
  PyObject * events2Ipixd_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    PyObject *pypixelPositions;
    long N;
    int pixel_begin, pixel_end, pixel_step;
    double d_begin, d_end, d_step;
    long ntotpixels=  (115)*8*128;
    
    double tofUnit = 1e-7;
    double mod2sample = 13.6;
    double emission_time = 0.0;
    
    int ok = PyArg_ParseTuple
      (args, "OliiidddOO|lddd", 
       &pyevents, &N, 
       &pixel_begin, &pixel_end, &pixel_step,
       &d_begin, &d_end, &d_step,
       &pyintensities,
       &pypixelPositions,
       &ntotpixels, &tofUnit,
       &mod2sample, &emission_time);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );

    Event2pixd e2pixd
      (pixelPositions, ntotpixels, tofUnit, mod2sample, emission_time );

    /*
    std::cout << "pixel axis" 
	      << pixel_begin << ", "
	      << pixel_end << ", "
	      << pixel_step << ", "
	      << std::endl;
    std::cout << "E axis" 
	      << d_begin << ", "
	      << d_end << ", "
	      << d_step << ", "
	      << std::endl;
    */
    return events2EvenlySpacedIxy_impl::call_numpyarray
      <Event2pixd,
      unsigned int, double, npy_int, NPY_INT>
      (e2pixd,
       pyevents, N,
       pixel_begin, pixel_end, pixel_step, 
       d_begin, d_end, d_step, 
       pyintensities)
      ;
  }
  

} // wrap_arcseventdata:



// version
// $Id$

// End of file
