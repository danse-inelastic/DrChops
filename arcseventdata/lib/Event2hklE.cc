#include <cmath>
#include <iostream>
#include "Event.h"
#include "Event2hklE.h"
#include "conversion.h"
#ifdef DEBUG
#include "journal/debug.h"
#endif


namespace ARCS_EventData {

  namespace Event2hklE_impl {
    const char jrnltag[] = "Event2hklE";
  }


  Event2hklE::Event2hklE
    ( double Ei,
      double *ub,
      const double * pixelPositions, unsigned int ntotpixels,
      double tofUnit, double mod2sample, double toffset ) 
      : m_ev2qqqe(Ei, pixelPositions, ntotpixels, tofUnit, mod2sample, toffset)
  {
    for (int i=0; i<9; i++) m_ub_store[i] = ub[i];

    m_ub[0] = m_ub_store;
    m_ub[1] = m_ub_store + 3;
    m_ub[2] = m_ub_store + 6;
  }
  
  unsigned int
  Event2hklE::operator ()
    ( const Event & e, double &h, double &k, double &l, double &E ) const
  {
    static double Qx, Qy, Qz;
    
    if (m_ev2qqqe(e, Qx, Qy, Qz, E)==0) return 0;
    
    h = m_ub[0][0]*Qx + m_ub[0][1]*Qy + m_ub[0][2]*Qz;
    k = m_ub[1][0]*Qx + m_ub[1][1]*Qy + m_ub[1][2]*Qz;
    l = m_ub[2][0]*Qx + m_ub[2][1]*Qy + m_ub[2][2]*Qz;

    return 1;
  }
  
}


