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


#ifndef H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIX
#define H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIX


//#include "events2Ix.h"
#include "Histogrammer.h"
#include "events2histogram.h"
#include "histogram/EvenlySpacedGridData_1D.h"


namespace ARCS_EventData{

  struct Event;
  
  /// add events to histogram I(x); x is an evenly spaced axis.
  ///
  /// template arguments:
  ///   Event2X: a Event2Quantity class
  //    XData: data type of x 
  ///   YIterator: iterator of y values.
  //    EventIterator: event iterator type.
  /// 
  /// arguments:
  ///   events: neutron events
  ///   N: number of neutron events to be processed
  ///   e2x: event -> x functor
  ///   x_begin, x_end, x_step: define the x axis
  ///   y_begin: iterator of y array to store y values at x points on x axis
  template <typename Event2X, 
	    typename XData,
	    typename YData, typename YIterator,
	    typename EventIterator>
  void events2EvenlySpacedIx
  ( const EventIterator events_begin, size_t N, const Event2X & e2x, 
    XData x_begin, XData x_end, XData x_step, 
    YIterator y_begin)
  {
    typedef EvenlySpacedGridData_1D< XData, YData, YIterator> Ix;
    Ix ix(x_begin, x_end, x_step, y_begin);
    
    Histogrammer1< Event, Ix, Event2X, 
      typename Ix::xdatatype, typename Ix::ydatatype> her( ix, e2x );
    events2histogram( events_begin, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIX


// version
// $Id$

// End of file 
  
