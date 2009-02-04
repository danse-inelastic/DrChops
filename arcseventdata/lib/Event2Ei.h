// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2009  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_ARCS_EVENTDATA_EVENT2EI
#define H_ARCS_EVENTDATA_EVENT2EI

#include "Event2Quantity.h"

/// Convert neutron Event to d-spacing
/// Most useful for reduction of diffraction data.


namespace ARCS_EventData {
  
  struct Event;

  
  /// Event2Ei: calculated incident energy of an event.
  /// Functor to calculate incident neutron energy of an neutron event.
  /// The is most useful if we can assume that the scattering are elastic.
  /// For example, diffraction from Silicon, etc. The incident beam
  /// is a white beam.
  class Event2Ei: public Event2Quantity1<double> {

  public:
    /// ctor.
    /// Constructor. 
    /// pixelPositions: mapping of pixelID --> position 
    ///     pixelPositions[pixelID*3, pixelID*3+1, pixelID*3+2] is the position vector
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    /// mod2sample: distance from moderator to sample. unit: meter
    Event2Ei( const double * pixelPositions, unsigned int ntotpixels = (1+115)*8*128,
	     double tofUnit=1e-7, double mod2sample=13.5 ) 
      : m_pixelPositions( pixelPositions ), m_tofUnit( tofUnit ),
	m_mod2sample( mod2sample ), m_ntotpixels(ntotpixels)
    {
      //std::cout << "Event2Ei ctor: pixelPositions = " << pixelPositions << std::endl;
      /*
      std::cout << "mod2sample distance = " << m_mod2sample << std::endl;
      std::cout << "number of total pixels = " << m_ntotpixels << std::endl;
      */
    }
    
    virtual unsigned int operator () ( const Event & e, double &Ei ) const;
      
  private:

    const double * m_pixelPositions;
    double m_tofUnit;
    double m_mod2sample;
    double m_ntotpixels;
  };
  
}


#endif// H_ARCS_EVENTDATA_EVENT2EI


// version
// $Id$

// End of file 
  
