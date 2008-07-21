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


#ifndef H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXXXX
#define H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXXXX

//#include "events2Ixxxx.h"
#include "Histogrammer.h"
#include "events2histogram.h"
#include "histogram/EvenlySpacedGridData_4D.h"


namespace ARCS_EventData{

  struct Event;
  
  /// add events to histogram I(x1,x2,x3,x4); {xi}, i=1..4 are evenly spaced axes.
  ///
  /// template arguments:
  ///   Event2XXXX: a Event2Quantity4 class
  //    X1Data: data type of x1 
  //    X2Data: data type of x2 
  //    X3Data: data type of x3 
  //    X4Data: data type of x4 
  ///   ZIterator: iterator of z values.
  //    EventIterator: event iterator type.
  /// 
  /// arguments:
  ///   events_begin: begin iterator of neutron events 
  ///   N: number of neutron events to be processed
  ///   e2xxxx: event -> x functor
  ///   xi_begin, xi_end, xi_step: define the xi axis
  ///   z_begin: iterator of z array to store z values on the grid defined
  ///            by {xi} axes
  template <typename Event2XXXX, 
	    typename X1Data, typename X2Data, typename X3Data, typename X4Data,
	    typename ZData, typename ZIterator,
	    typename EventIterator>
  void events2EvenlySpacedIxxxx
  ( const EventIterator events_begin, size_t N, const Event2XXXX & e2xxxx, 
    X1Data x1_begin, X1Data x1_end, X1Data x1_step, 
    X2Data x2_begin, X2Data x2_end, X2Data x2_step, 
    X3Data x3_begin, X3Data x3_end, X3Data x3_step, 
    X4Data x4_begin, X4Data x4_end, X4Data x4_step, 
    ZIterator z_begin)
  {
    typedef EvenlySpacedGridData_4D< X1Data, X2Data, X3Data, X4Data, ZData, ZIterator> Ixxxx;
    Ixxxx ixxxx
      (x1_begin, x1_end, x1_step, 
       x2_begin, x2_end, x2_step, 
       x3_begin, x3_end, x3_step, 
       x4_begin, x4_end, x4_step, 
       z_begin);
    
    Histogrammer4< Event, Ixxxx, Event2XXXX, 
      X1Data, X2Data, X3Data, X4Data, ZData>  her( ixxxx, e2xxxx );
    events2histogram( events_begin, N, her );
    return ;
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2EVENLYSPACEDIXXXX


// version
// $Id$

// End of file 
  
