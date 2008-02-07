#include <math.h>
#include <iostream>
#include "Event.h"
#include "Event2d.h"
#include "conversion.h"

#ifdef DEBUG
#include "journal/debug.h"
#endif
#include "journal/warning.h"

namespace ARCS_EventData {
  
  namespace Event2d_Impl {
    const char jrnltag[] = "Event2d";
  }

  bool
  Event2d::operator ()
    ( const Event & e, double &d ) const
  {
    const unsigned int & pixelID = e.pixelID;
    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
      journal::warning_t warning( Event2d_Impl::jrnltag );
      warning << journal::at(__HERE__)
	      << "pixel ID out of bound: " << pixelID 
	      << journal::endl;
#endif
      return 1;
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
    double lambda = 2*pi/(velocity * V2K);

    // twothea
    // note: assuming we use "Instrument scientist" coord system
    // z: up (opposite of gravity)
    // x: neutron beam downstream
    double twotheta = acos( x / sample2pixel );

    // d spacing: Bragg's law
    d = lambda/2/sin(twotheta/2);

    //std::cout << "pixelID=" << pixelID << ", x,y,z=" << x << "," << y << "," << z << ", sample2pixel = " << sample2pixel << ", mo2sample=" << m_mod2sample << "tof = " << tof << "velocity = " << velocity << "lambda=" << lambda << "twotheta = " << twotheta << ", d = " << d << std::endl;

    return 0;
  }
  
}


