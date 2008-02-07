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


#ifndef H_ARCSEVENTDATA_MAPPERS
#define H_ARCSEVENTDATA_MAPPERS

#include "Event2Quantity.h"

namespace ARCS_EventData{

  class Event2TofChannel: public Event2Quantity1<unsigned int>
  {
  public:
    bool operator() ( const Event & e, unsigned int & d ) const 
    {
      d = e.tof;
      return 0;
    }
  };
  
  const Event2TofChannel e2tc;


  class Event2pixelID: public Event2Quantity1<unsigned int>
  {
  public:
    bool operator() ( const Event & e, unsigned int & d ) const 
    {
      d = e.pixelID;
      return 0;
    }
  };
  
  const Event2pixelID e2pixelID;

  class Event2pixelIDtofChannel: public Event2Quantity2<unsigned int, unsigned int>
  {
  public:
    bool operator() ( const Event & e, unsigned int & pixelID, unsigned int & tof ) const 
    {
      pixelID = e.pixelID;
      tof = e.tof;
      return 0;
    }
  };
  
  const Event2pixelIDtofChannel e2pt;

}


#endif // H_ARCSEVENTDATA_MAPPERS


// version
// $Id$

// End of file 
  
