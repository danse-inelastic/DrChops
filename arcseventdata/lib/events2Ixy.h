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


#ifndef H_ARCSEVENTDATA_EVENTS2IXY
#define H_ARCSEVENTDATA_EVENTS2IXY

#include "Histogrammer.h"
#include "events2histogram.h"

namespace ARCS_EventData{

  struct Event;
  
  /// Function to histogramming neutron events to I(x,y) histogram.
  /// events2Ix is a function that histograms neutron events (objects
  /// of class Event) in to a 2D histogram.
  ///
  /// template arguments:
  ///   Event2XY: a Event2Quantity2 class
  ///   Ixy: a DataGrid2D class or a Ixy class
  /// 
  /// arguments:
  ///   events: neutron events
  ///   N: number of neutron events to be processed
  ///   e2xy: event -> x,y functor
  ///   ixy: I(x,y) histogram
  template <typename Event2XY, typename Ixy, typename EventIterator>
  void events2Ixy
  ( const EventIterator events_begin, size_t N, const Event2XY & e2xy, Ixy & ixy )
  {
    Histogrammer2< Ixy, Event2XY, typename Ixy::xdatatype, typename Ixy::ydatatype> 
      her( ixy, e2xy );
    events2histogram( events_begin, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2IX


// version
// $Id$

// End of file 
  
