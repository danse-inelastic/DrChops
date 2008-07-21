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


#ifndef H_ARCSEVENTDATA_EVENT2QUANTITY
#define H_ARCSEVENTDATA_EVENT2QUANTITY

namespace ARCS_EventData{

  struct Event;

  /// Event2Quantity1: convert event to a scalar quantity.
  /// Class to convert an neutron event (Event object) to a scalar quantity.
  /// For example, 
  ///   * event --> pixel ID
  ///   * event --> tof
  /// This is an abstract base class. 
  /// Solid subclasses will be used by histogrammers (objects of Histogrammer1). 
  template <typename DataType>
  class Event2Quantity1 {
  public:
    /// convert event to a quantity
    /// return: 0 if failed. 1 if succeed
    virtual unsigned int operator() ( const Event & e, DataType & d ) const = 0;
    virtual ~Event2Quantity1() {} ;
  };

  /// Event2Quantity2: convert event to two scalar quantities.
  /// Class to convert an neutron event (Event object) to two scalar quantities.
  /// Forexample, 
  ///   event --> pixel ID, tof
  ///   event --> Q, E
  /// This is an abstract base class.
  /// Solid subclasses will be used by histogrammers (objects of Histogrammer2). 
  template <typename DataType1, typename DataType2>
  class Event2Quantity2 {
  public:
    /// convert event to two quantities
    /// return: 0 if failed. 1 if succeed
    virtual unsigned int operator() ( const Event & e, DataType1 & d1, DataType2 &d2 ) const = 0;
    virtual ~Event2Quantity2() {}
  };

  /// Event2Quantity4: convert event to four scalar quantities.
  /// Class to convert an neutron event (Event object) to four scalar quantities.
  /// Forexample, 
  ///   event --> Qx, Qy, Qz, E
  /// This is an abstract base class.
  /// Solid subclasses will be used by histogrammers (objects of Histogrammer4). 
  template <typename DataType1, typename DataType2, typename DataType3, typename DataType4>
  class Event2Quantity4 {
  public:
    /// convert event to 4 quantities
    /// return: 0 if failed. 1 if succeed
    virtual unsigned int operator() ( const Event & e, 
			      DataType1 & d1, DataType2 &d2, DataType3 &d3, DataType4 &d4  ) const = 0;
    virtual ~Event2Quantity4() {}
  };

}


#endif // H_ARCSEVENTDATA_EVENT2QUANTITY


// version
// $Id$

// End of file 
