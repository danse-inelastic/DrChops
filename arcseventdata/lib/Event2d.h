#ifndef H_ARCS_EVENTDATA_EVENT2D
#define H_ARCS_EVENTDATA_EVENT2D

#include "Event2Quantity.h"

/// Convert neutron Event to d-spacing
/// Most useful for reduction of diffraction data.


namespace ARCS_EventData {
  
  struct Event;

  
  /// Event2d: calculated d-spacing (diffraction) of an event.
  /// Functor to calculate d-spacing from neutron event.
  /// The is most useful for diffraction reduction.
  /// The Bragg's law: 2dsintheta = lambda
  /// so d = lambda/2sintheta.
  /// lambda can be infered from tof, and 2theta is the scattering angle.
  /// This is a fairly easy computation.
  class Event2d: public Event2Quantity1<double> {

  public:
    /// ctor.
    /// Constructor. 
    /// pixelPositions: mapping of pixelID --> position 
    ///     pixelPositions[pixelID*3, pixelID*3+1, pixelID*3+2] is the position vector
    /// tofUnit: unit of tof. for example, for 100ns, tofUnit = 1e-7
    /// mod2sample: distance from moderator to sample. unit: meter
    Event2d( const double * pixelPositions, unsigned int ntotpixels = (1+115)*8*128,
	     double tofUnit=1e-7, double mod2sample=13.5 ) 
      : m_pixelPositions( pixelPositions ), m_tofUnit( tofUnit ),
	m_mod2sample( mod2sample ), m_ntotpixels(ntotpixels)
    {
      //std::cout << "Event2d ctor: pixelPositions = " << pixelPositions << std::endl;
      /*
      std::cout << "mod2sample distance = " << m_mod2sample << std::endl;
      std::cout << "number of total pixels = " << m_ntotpixels << std::endl;
      */
    }
    
    virtual bool operator () ( const Event & e, double &d ) const;
      
  private:

    const double * m_pixelPositions;
    double m_tofUnit;
    double m_mod2sample;
    double m_ntotpixels;
  };
  
}


#endif// H_ARCS_EVENTDATA_EVENT2D
