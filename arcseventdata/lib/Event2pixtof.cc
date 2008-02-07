#include <cmath>
#include <iostream>
#include "Event.h"
#include "Event2pixtof.h"
#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace ARCS_EventData {

  namespace Event2pixtof_impl {
    const char jrnltag[] = "Event2pixtof";
  }

  Event2pixtof::Event2pixtof
    (unsigned int ntotpixels, double tofUnit) 
    : m_tofUnit( tofUnit ),
      m_ntotpixels(ntotpixels)
  {
  }
  
  bool
  Event2pixtof::operator ()
    ( const Event & e, unsigned int &pixelID, double &tof ) const
  {
    pixelID = e.pixelID;
    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
    journal::debug_t debug( Event2pixtof_impl::jrnltag );
    debug << journal::at(__HERE__)
	  << "pixel ID out of bound: " << pixelID
	  << journal::endl;
#endif
      return 1;
    }
    const unsigned int & tofchannelno = e.tof;
    
    // tof in seconds
    tof = tofchannelno*m_tofUnit;

    return 0;
  }
  
}


