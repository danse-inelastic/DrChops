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


#ifndef H_ARCSEVENTDATA_EVENT2PIXEI
#define H_ARCSEVENTDATA_EVENT2PIXEI

#include "Event2Quantity.h"

namespace ARCS_EventData{

  // Event -> pixelID, energy transfer
  class Event2pixEi: public Event2Quantity2<unsigned int, double>
  {
  public:
    // meta methods
    /// ctor.
    /// Constructor. 
    /// pixelPositions: mapping of pixelID --> position 
    ///     pixelPositions[pixelID*3, pixelID*3+1, pixelID*3+2] is the position vector
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    /// mod2sample: distance from moderator to sample. unit: meter
    Event2pixEi
    (const double * pixelPositions, 
      unsigned int ntotpixels = (1+115)*8*128,
      double tofUnit=1e-7, double mod2sample=13.5,
      double emission_time = 0.0
      );

    // methods
    unsigned int operator() ( const Event & e, unsigned int & pixelID, double & Ei ) const ;


  private:

    //data
    const double * m_pixelPositions;
    double m_tofUnit;
    double m_mod2sample;
    double m_ntotpixels;
    double m_emission_time;
  };
  
}


#endif // H_ARCSEVENTDATA_EVENT2PIXEI


// version
// $Id$

// End of file 
  
