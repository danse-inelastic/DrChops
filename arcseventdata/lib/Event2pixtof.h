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


#ifndef H_ARCSEVENTDATA_EVENT2PIXTOF
#define H_ARCSEVENTDATA_EVENT2PIXTOF

#include "Event2Quantity.h"

namespace ARCS_EventData{

  // Event -> pixelID, tof
  class Event2pixtof: public Event2Quantity2<unsigned int, double>
  {
  public:
    // meta methods
    /// ctor.
    /// Constructor. 
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    Event2pixtof
    (unsigned int ntotpixels = (1+115)*8*128,
     double tofUnit=1e-7);

    // methods
    unsigned int operator() ( const Event & e, unsigned int & pixelID, double & tof ) const ;


  private:

    //data
    double m_tofUnit;
    double m_ntotpixels;
  };
  
}


#endif // H_ARCSEVENTDATA_EVENT2PIXTOF


// version
// $Id$

// End of file 
  
