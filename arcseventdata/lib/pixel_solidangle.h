// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2008  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_ARCS_EVENTDATA_PIXEL_SOLIDANGLE
#define H_ARCS_EVENTDATA_PIXEL_SOLIDANGLE


namespace ARCS_EventData{

  // calcualte solid angle for ARCS detector pixels
  // ARCS detectors are installed vertically, so the solid angle
  // of a pixel can be determined by its position relative to the sample
  // coordinate system.
  //  x: downstream
  //  z: vertical up
  template <typename Float>
  Float pixel_solidangle( Float area, Float x, Float y, Float z ) ;

}// ARCS_EventData


#include "pixel_solidangle.icc"

#endif 


// version
// $Id$

// End of file 
