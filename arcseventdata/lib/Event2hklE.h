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


#ifndef H_ARCSEVENTDATA_EVENT2HKLE
#define H_ARCSEVENTDATA_EVENT2HKLE

#include "Event2Quantity.h"

#include "Event2QQQE.h"

namespace ARCS_EventData{

  // Event -> h,k,l, E
  class Event2hklE: public Event2Quantity4<double, double, double, double>
  {
  public:
    // meta methods
    /// ctor.
    /// Constructor. 
    /// Ei: neutron incident energy. meV
    /// ub: matrix to convert Q vector to hkl. stored as a 9-elements double array
    /// pixelPositions: mapping of pixelID --> position 
    ///     pixelPositions[pixelID*3, pixelID*3+1, pixelID*3+2] is the position vector
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    /// mod2sample: distance from moderator to sample. unit: meter
    /// tofset: shutter tof offset
    Event2hklE
    ( double Ei,
      double *ub,
      const double * pixelPositions, 
      unsigned int ntotpixels = (1+115)*8*128,
      double tofUnit=1e-7, double mod2sample=13.5,
      double toffset = 0.0
      );

    // methods
    unsigned int operator() ( const Event & e, double &h, double &k, double &l, double & E ) const ;


  private:

    //data
    Event2QQQE m_ev2qqqe;
    double m_ub_store[9];
    double *m_ub[3];
  };
  
}


#endif // H_ARCSEVENTDATA_EVENT2HKLE


// version
// $Id$

// End of file 
  
