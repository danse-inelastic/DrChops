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


#ifndef H_ARCSEVENTDATA_EVENTS2IX
#define H_ARCSEVENTDATA_EVENTS2IX

#include "Histogrammer.h"
#include "events2histogram.h"

namespace ARCS_EventData{

  struct Event;
  
  /// add events to histogram I(x).
  ///
  /// template arguments:
  ///   Event2X: a Event2Quantity class
  ///   Ix: a GridData_1D class
  ///   EventIterator: event iterator type
  /// 
  /// arguments:
  ///   events: neutron events
  ///   N: number of neutron events to be processed
  ///   e2x: event -> x functor
  ///   ix: I(x) histogram
  template <typename Event2X, typename Ix, typename EventIterator>
  void events2Ix
  ( const EventIterator events_begin, size_t N, const Event2X & e2x, Ix & ix )
  {
    Histogrammer1< Event, Ix, Event2X, typename Ix::xdatatype, typename Ix::ydatatype> her( ix, e2x );
    events2histogram( events_begin, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2IX


// version
// $Id$

// End of file 
  
