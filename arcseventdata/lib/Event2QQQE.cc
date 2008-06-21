#include <cmath>
#include <iostream>
#include "Event.h"
#include "Event2QQQE.h"
#include "conversion.h"
#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace ARCS_EventData {

  namespace Event2QQQE_impl {
    const char jrnltag[] = "Event2QQQE";
  }


  Event2QQQE::Event2QQQE
    ( double Ei,
      const double * pixelPositions, unsigned int ntotpixels,
      double tofUnit, double mod2sample, double toffset ) 
      : m_Ei(Ei), m_vi( std::sqrt(Ei) * SE2V ), m_ki(m_vi*V2K),
	m_pixelPositions( pixelPositions ), m_tofUnit( tofUnit ),
	m_mod2sample( mod2sample ), m_ntotpixels(ntotpixels),
	m_toffset( toffset*1.e-6 )
  {
#ifdef DEBUG
    journal::debug_t debug( Event2QQQE_impl::jrnltag );
    debug << journal::at(__HERE__)
	  << "m_pixelPositions=" << m_pixelPositions 
	  << journal::endl;
#endif
  }
  
  bool
  Event2QQQE::operator ()
    ( const Event & e, double &Qx, double &Qy, double &Qz, double &E ) const
  {
    const unsigned int & pixelID = e.pixelID;

    if (pixelID<0 || pixelID>=m_ntotpixels) {
#ifdef DEBUG
      journal::debug_t debug( Event2QQQE_impl::jrnltag );
      debug << journal::at(__HERE__)
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

    // tof total in second
    double toftotal = tofchannelno * m_tofUnit;
    // this is a hack. The moderator frequency is 60 Hz
    // so any data with tof > 1/60. should be not real
    if (toftotal>0.01500) {
#ifdef DEBUG
      journal::debug_t debug( Event2QQQE_impl::jrnltag );
      debug << journal::at(__HERE__)
	    << "tof out of range: "  << toftotal
	    << journal::endl;
#endif
      return 1;
    }

    // tof from sample to pixel in second
    double tof = toftotal - m_toffset - m_mod2sample/m_vi;
    if (tof<0) {
#ifdef DEBUG
      journal::debug_t debug( Event2QQQE_impl::jrnltag );
      debug << journal::at(__HERE__)
	    << "negative time of flight" << tof 
	    << journal::endl;
#endif
      return 1;
    }

    // distances in meter
    double sample2pixel = sqrt(x*x+y*y+z*z);

    // velocity of final neutron
    double velocity = sample2pixel/tof;

    // final energy of neutron
    double Ef = VS2E * velocity * velocity;
    
    // energy transfer
    E = m_Ei - Ef;

    // kf vector
    double t = velocity*V2K/sample2pixel, kx = x*t, ky = y*t, kz = z*t;

    // Q vector
    Qx = m_ki-kx;
    Qy = -ky;
    Qz = -kz;
    
    //std::cout << "pixelID=" << pixelID << ", x,y,z=" << x << "," << y << "," << z << ", sample2pixel = " << sample2pixel << ", mo2sample=" << m_mod2sample << "tof = " << tof << "velocity = " << velocity << "k=" << kx << ',' << ky << ',' << kz << "ki = " << m_ki << ", Q = " << Q << std::endl;
    return 0;
  }
  
}


