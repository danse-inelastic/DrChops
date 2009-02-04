#include <math.h>
#include <iostream>
#include "Event.h"
#include "Event2Ei.h"
#include "conversion.h"

#ifdef DEBUG
#include "journal/debug.h"
#endif
#include "journal/warning.h"

namespace ARCS_EventData {
  
  namespace Event2Ei_Impl {
    const char jrnltag[] = "Event2Ei";
  }

  unsigned int
  Event2Ei::operator ()
    ( const Event & e, double &Ei ) const
  {
    const unsigned int & pixelID = e.pixelID;
    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
      journal::warning_t warning( Event2Ei_Impl::jrnltag );
      warning << journal::at(__HERE__)
	      << "pixel ID out of bound: " << pixelID 
	      << journal::endl;
#endif
      return 0;
    }
    const unsigned int & tofchannelno = e.tof;

    // pixel position
    const double *ppos = m_pixelPositions + 3*pixelID;
    const double &x = *ppos;
    const double &y = *(ppos+1);
    const double &z = *(ppos+2);

    // tof in second
    double tof = tofchannelno * m_tofUnit;

    // distances in meter
    double sample2pixel = sqrt(x*x+y*y+z*z);

    // velocity of neutron
    double velocity = (m_mod2sample+sample2pixel)/tof;

    // wavelength of neutron
    //double lambda = 2*pi/(velocity * V2K);

    // energy of neutron
    Ei = velocity*velocity*VS2E;
    
    return 1;
  }
  
}


