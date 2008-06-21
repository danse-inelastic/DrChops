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
#include "wrap_events2EvenlySpacedIxxxx.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/Event2Quantity.h"
#include "arcseventdata/events2EvenlySpacedIxxxx.h"

#include "arcseventdata/Event2QQQE.h"


#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace wrap_arcseventdata
{

  namespace wrap_events2EvenlySpacedIxxxx_Impl {
    const char jrnltag[] = "events2EvenlySpacedIxxxx";
  }
  
  using namespace ARCS_EventData;
  using namespace reductionmod;
  
  typedef Array1DIterator<npy_double> DblArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  
  namespace events2EvenlySpacedIxxxx_impl {
    
    template <typename Event2XXXX, 
	      typename X1Data, typename X2Data, typename X3Data, typename X4Data,
	      typename ZData, int ZTypeCode
	      >
    PyObject * call_numpyarray
    (const Event2XXXX & e2xxxx,
     PyObject * pyevents, size_t N,
     X1Data x1_begin, X1Data x1_end, X1Data x1_step, 
     X2Data x2_begin, X2Data x2_end, X2Data x2_step, 
     X3Data x3_begin, X3Data x3_end, X3Data x3_step, 
     X4Data x4_begin, X4Data x4_end, X4Data x4_step, 
     PyObject *pyzarray)
    {
      if (checkDataType(pyzarray, "zarray", ZTypeCode)) return 0;

      std::ostringstream oss;

      const Event *events_begin = (const Event *)
	PyCObject_AsVoidPtr( pyevents );
#ifdef DEBUG
      journal::debug_t debug( wrap_events2EvenlySpacedIxxxx_Impl::jrnltag );
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
      size_t tmpsize =  size_t((x1_end-x1_begin)/x1_step) * size_t( (x2_end-x2_begin)/x2_step)
	* size_t((x3_end-x3_begin)/x3_step) * size_t( (x4_end-x4_begin)/x4_step);
      
      if (nzarrsize != tmpsize )  {
	oss << "Size mismatch: "
	    << "zarray: size = " << nzarrsize << "; "
	    << "x1 bin boundaries parameters = " << x1_begin << ", " << x1_end << ", " << x1_step
	    << "x2 bin boundaries parameters = " << x2_begin << ", " << x2_end << ", " << x2_step
	    << "x3 bin boundaries parameters = " << x3_begin << ", " << x3_end << ", " << x3_step
	    << "x4 bin boundaries parameters = " << x4_begin << ", " << x4_end << ", " << x4_step
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
      
      events2EvenlySpacedIxxxx<Event2XXXX, X1Data, X2Data, X3Data, X4Data, ZData, ZIterator>
	(events_begin, N, e2xxxx, 
	 x1_begin, x1_end, x1_step, 
	 x2_begin, x2_end, x2_step, 
	 x3_begin, x3_end, x3_step, 
	 x4_begin, x4_end, x4_step, 
	 z_begin);

      return Py_None;
    }
    
  }
 
  

  // 
  char events2IQQQE_numpyarray__name__[] = "events2IQQQE_numpyarray";
  char events2IQQQE_numpyarray__doc__[] = "events2IQQQE_numpyarray\n" \
"events2IQQQE( events, N, \n"\
"            Qx_begin, Qx_end, Qx_step, \n"\
"            Qy_begin, Qy_end, Qy_step, \n"\
"            Qz_begin, Qz_end, Qz_step, \n"\
"            E_begin, E_end, E_step, \n"\
"            intensities, Ei, pixelPositions, ntotpixels, tofUnit, \n"\
"            mod2sample, toffset)"
;
  // events: PyCObject of pointer to events
  // N: number of events to process
  // Qx_begin, Qx_end, Qx_step: Qx axis parameters
  // Qy_begin, Qy_end, Qy_step: Qy axis parameters
  // Qz_begin, Qz_end, Qz_step: Qz axis parameters
  // E_begin, E_end, E_step: E axis parameters
  // intensities: numpy array to store I(d)
  // Ei: incident neutron energy
  // pixelPositions: double * pointer to pixel positions 
  // ntotpixels: number of total pixels. actually (npack+1)*ndetsperpack*npixelsperdet
  // tofUnit: unit of tof in the event data file
  // mod2sample: moderator sample distance. unit: meter
  // toffset: shutter time offset. unit: microsecond
  
  PyObject * events2IQQQE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyevents, *pyintensities;
    long N;
    double Qx_begin, Qx_end, Qx_step;
    double Qy_begin, Qy_end, Qy_step;
    double Qz_begin, Qz_end, Qz_step;
    double E_begin, E_end, E_step;
    double Ei;
    PyObject *pypixelPositions;
    long ntotpixels=  115*8*128;
    double tofUnit = 1e-7, mod2sample = 13.5;
    double toffset = 0;
    
    int ok = PyArg_ParseTuple
      (args, "OlddddddddddddOdO|lddd", 
       &pyevents, &N, 
       &Qx_begin, &Qx_end, &Qx_step,
       &Qy_begin, &Qy_end, &Qy_step,
       &Qz_begin, &Qz_end, &Qz_step,
       &E_begin, &E_end, &E_step,
       &pyintensities,
       &Ei,
       &pypixelPositions, 
       &ntotpixels, &tofUnit, &mod2sample,
       &toffset);
    
    if (!ok) return 0;
    
    const double * pixelPositions = static_cast<const double *>
      ( PyCObject_AsVoidPtr( pypixelPositions ) );
    Event2QQQE e2QQQE( Ei, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset );
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
    return events2EvenlySpacedIxxxx_impl::call_numpyarray
      <Event2QQQE,
      double, double, double, double, npy_int, NPY_INT>
      (e2QQQE,
       pyevents, N,
       Qx_begin, Qx_end, Qx_step, 
       Qy_begin, Qy_end, Qy_step, 
       Qz_begin, Qz_end, Qz_step, 
       E_begin, E_end, E_step, 
       pyintensities)
      ;
  }
  
} // wrap_arcseventdata:



// version
// $Id$

// End of file
