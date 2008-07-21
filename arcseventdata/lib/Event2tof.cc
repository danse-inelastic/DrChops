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


#include <iostream>

#include "Event.h"
#include "Event2tof.h"
#ifdef DEBUG
#include "journal/debug.h"
#endif



namespace ARCS_EventData{

  namespace Event2tof_impl {
    const char jrnltag[] = "Event2tof";
  }


  Event2tof::Event2tof
  (unsigned int ntotpixels, double tofUnit)
    : m_tofUnit( tofUnit ), m_ntotpixels( ntotpixels )
  {
  }

  unsigned int 
  Event2tof::operator() ( const Event & e, double & tof) const 
  {
    const unsigned int &pixelID = e.pixelID;
    
    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
      journal::debug_t debug( Event2tof_impl::jrnltag );
      debug << journal::at(__HERE__)
	    << "pixel ID out of bound: " << pixelID
	    << journal::endl;
#endif
      return 0;
    }
    const unsigned int & tofchannelno = e.tof;
    
    // tof in seconds
    tof = tofchannelno*m_tofUnit;
    return 1;
  }
}


// version
// $Id$

// End of file 
  
