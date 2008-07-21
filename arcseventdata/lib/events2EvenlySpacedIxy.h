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


#ifndef H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXY
#define H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXY

//#include "events2Ixy.h"
#include "Histogrammer.h"
#include "events2histogram.h"
#include "histogram/EvenlySpacedGridData_2D.h"

namespace ARCS_EventData{

  struct Event;
  
  /// add events to histogram I(x,y); both x and y are evenly spaced axes.
  ///
  /// template arguments:
  ///   Event2XY: a Event2Quantity2 class
  //    XData: data type of x 
  //    YData: data type of y 
  ///   ZIterator: iterator of z values.
  //    EventIterator: event iterator type.
  /// 
  /// arguments:
  ///   events_begin: begin iterator of neutron events 
  ///   N: number of neutron events to be processed
  ///   e2xy: event -> x functor
  ///   x_begin, x_end, x_step: define the x axis
  ///   y_begin, y_end, y_step: define the y axis
  ///   z_begin: iterator of z array to store z values on the grid defined
  ///            by x and y axes
  template <typename Event2XY, 
	    typename XData, typename YData,
	    typename ZData, typename ZIterator,
	    typename EventIterator>
  void events2EvenlySpacedIxy
  ( const EventIterator events_begin, size_t N, const Event2XY & e2xy, 
    XData x_begin, XData x_end, XData x_step, 
    YData y_begin, YData y_end, YData y_step, 
    ZIterator z_begin)
  {
    typedef EvenlySpacedGridData_2D< XData, YData, ZData, ZIterator> Ixy;
    Ixy ixy
      (x_begin, x_end, x_step, 
       y_begin, y_end, y_step, 
       z_begin);
    
    Histogrammer2< Event, Ixy, Event2XY, XData, YData, ZData> her( ixy, e2xy );
    events2histogram( events_begin, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXY


// version
// $Id$

// End of file 
  
