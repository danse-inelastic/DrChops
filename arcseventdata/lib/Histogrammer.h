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
  template <typename Event, typename GridData_1D, typename Event2Quantity1, 
	    typename DataType, typename IDataType>
  class Histogrammer1 {
    
  public:
    Histogrammer1( GridData_1D & fx, const Event2Quantity1 & e2x )
      : m_fx( fx ), m_e2x( e2x )
    {
    }
    
    void operator() ( const Event & e )
    {
      IDataType i = m_e2x( e, m_x );
      if (m_fx.isOutofbound(m_x)) {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer1");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << m_x
		<< journal::endl;
#endif
	return;
      }
      try {
	m_fx( m_x ) += i;
      } catch (OutOfBound err) {
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
  template <typename Event, typename GridData_2D, typename Event2Quantity2, 
	    typename XDataType, typename YDataType,
	    typename IDataType>
  class Histogrammer2 {
    
  public:
    Histogrammer2( GridData_2D & fxy, const Event2Quantity2 & e2xy )
      : m_fxy( fxy ), m_e2xy( e2xy )
    {
    }
    
    void operator() ( const Event & e )
    {
      IDataType i = m_e2xy( e, m_x, m_y );
      if (m_fxy.isOutofbound(m_x, m_y)) {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer2");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << m_x << ", " << m_y
		<< journal::endl;
#endif
	return;
      }
      try {
	m_fxy( m_x, m_y ) += i;
      } catch (OutOfBound err) {
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


  /// Histogammer4: add event to a 4D histogram.
  /// Class to add neutron events (objects of Event class) 
  /// to a 4-D histogram (object of GridData_4D).
  /// This is the core of event-mode reduction.
  /// The idea is, given a neutron event, the histogrammer
  /// deduce the values of the physical quantities from that neutron event, 
  /// and then do histogramming by add 1 to the bin
  /// to which the values of the physical quantities belong.
  ///
  /// template arguments:
  ///   GridData_4D: f(x1,x2,x3,x4) histogram. 
  ///   Event2Quantity4: functor event-->x1,x2,x3,x4
  ///   X1DataType: data type of x1
  ///   X2DataType: data type of x2
  ///   X3DataType: data type of x3
  ///   X4DataType: data type of x4
  ///
  template <typename Event, typename GridData_4D, typename Event2Quantity4, 
	    typename X1DataType, typename X2DataType, typename X3DataType, typename X4DataType,
	    typename IDataType>
  class Histogrammer4 {
    
  public:
    Histogrammer4( GridData_4D & fxxxx, const Event2Quantity4 & e2xxxx )
      : m_fxxxx( fxxxx ), m_e2xxxx( e2xxxx )
    {
    }
    
    void operator() ( const Event & e )
    {
      IDataType i = m_e2xxxx( e, m_x1, m_x2, m_x3, m_x4 );
      if (m_fxxxx.isOutofbound( m_x1, m_x2, m_x3, m_x4 )) {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer4");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << m_x1 << ", " << m_x2 << ", " << m_x3 << ", " << m_x4
		<< journal::endl;
#endif
	return;
      }
      try {
	m_fxxxx( m_x1, m_x2, m_x3, m_x4 ) += i;
      } catch (OutOfBound err) {
#ifdef DEBUG
	journal::warning_t warning("arcseventdata.Histogrammer4");
	warning << journal::at(__HERE__)
		<< "OutOfBound: " << err.what()
		<< journal::endl;
#endif
      }
    }
    
    void clear() 
    {
      m_fxxxx.clear();
    }

  private:
    GridData_4D & m_fxxxx;
    const Event2Quantity4 & m_e2xxxx;
    X1DataType m_x1;
    X2DataType m_x2;
    X3DataType m_x3;
    X4DataType m_x4;
  } ;

}


#endif // H_ARCSEVENTDATA_HISTOGRAMMER


// version
// $Id$

// End of file 
