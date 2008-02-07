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


#ifndef H_ARCSEVENTDATA_HISTOGRAMMER
#define H_ARCSEVENTDATA_HISTOGRAMMER

#include "histogram/OutOfBound.h"
#include "journal/warning.h"

namespace ARCS_EventData{

  using namespace DANSE::Histogram;

  struct Event;

  /// Histogammer1: add event to a 1D histogram.
  /// Class to add neutron events (objects of Event class) 
  /// to a 1-D histogram (object of GridData_1D).
  /// The is the core of event-mode reduction.
  /// The idea is, given a neutron event, the histogrammer
  /// deduce the value of the physical quantity from that neutron event, 
  /// and then do histogramming by add 1 to the bin
  /// to which the value of the physical quantity belongs.
  /// 
  /// template arguments:
  ///   GridData_1D: f(x) histogram. 1-dimensional
  ///   Event2Quantity1: functor event-->x
  ///   DataType: data type of x
  ///
  template <typename GridData_1D, typename Event2Quantity1, typename DataType>
  class Histogrammer1 {
    
  public:
    Histogrammer1( GridData_1D & fx, const Event2Quantity1 & e2x )
      : m_fx( fx ), m_e2x( e2x )
    {
    }
    
    void operator() ( const Event & e )
    {
      bool failed = m_e2x( e, m_x );
      if (failed) return;
      try {
	m_fx( m_x ) += 1;
      }
      catch (OutOfBound err)  {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer1");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << err.what()
		<< journal::endl;
#endif
      }
    }
    
    void clear() 
    {
      m_fx.clear();
    }

  private:
    GridData_1D & m_fx;
    const Event2Quantity1 & m_e2x;
    DataType m_x;
  } ;


  /// Histogammer2: add event to a 2D histogram.
  /// Class to add neutron events (objects of Event class) 
  /// to a 2-D histogram (object of GridData_2D).
  /// This is the core of event-mode reduction.
  /// The idea is, given a neutron event, the histogrammer
  /// deduce the values of the physical quantities from that neutron event, 
  /// and then do histogramming by add 1 to the bin
  /// to which the values of the physical quantities belong.
  ///
  /// template arguments:
  ///   GridData_2D: f(x,y) histogram. 
  ///   Event2Quantity2: functor event-->x,y
  ///   XDataType: data type of x
  ///   YDataType: data type of y
  ///
  template <typename GridData_2D, typename Event2Quantity2, 
	    typename XDataType, typename YDataType>
  class Histogrammer2 {
    
  public:
    Histogrammer2( GridData_2D & fxy, const Event2Quantity2 & e2xy )
      : m_fxy( fxy ), m_e2xy( e2xy )
    {
    }
    
    void operator() ( const Event & e )
    {
      if (m_e2xy( e, m_x, m_y )) return;
      try {
	m_fxy( m_x, m_y ) += 1;
      }
      catch (OutOfBound err)  {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer2");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << err.what()
		<< journal::endl;
#endif
      }
    }
    
    void clear() 
    {
      m_fxy.clear();
    }

  private:
    GridData_2D & m_fxy;
    const Event2Quantity2 & m_e2xy;
    XDataType m_x;
    YDataType m_y;
  } ;

}


#endif // H_ARCSEVENTDATA_HISTOGRAMMER


// version
// $Id$

// End of file 
