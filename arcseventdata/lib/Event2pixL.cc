#include <math.h>
#include <iostream>
#include "Event.h"
#include "Event2pixL.h"
#include "conversion.h"

#ifdef DEBUG
#include "journal/debug.h"
#endif
#include "journal/warning.h"

namespace ARCS_EventData {
  
  namespace Event2pixL_Impl {
    const char jrnltag[] = "Event2pixL";
  }

  Event2pixL::Event2pixL
  (const double * pixelPositions, unsigned int ntotpixels,
   double tofUnit, double mod2sample, double emission_time ) 
    : m_pixelPositions( pixelPositions ), m_tofUnit( tofUnit ),
      m_mod2sample( mod2sample ), m_ntotpixels(ntotpixels),
      m_emission_time( emission_time )
  {
  }


  unsigned int
  Event2pixL::operator ()
    ( const Event & e, unsigned int & pixelID, double &L ) const
  {
    pixelID = e.pixelID;
    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
      journal::warning_t warning( Event2pixL_Impl::jrnltag );
      warning << journal::at(__HERE__)
	      << "pixel ID out of bound: " << pixelID 
	      << journal::endl;
#endif
      return 0;
    }

    //calculate d
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

    // velocity of neutron: m/s
    double velocity = (m_mod2sample+sample2pixel)/tof;

    // wavelength of neutron: AA
    L = 2*pi/(velocity * V2K);

    return 1;
  }
  
}


