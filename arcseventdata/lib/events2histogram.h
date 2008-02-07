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


#ifndef H_ARCSEVENTDATA_EVENTS2HISTOGRAM
#define H_ARCSEVENTDATA_EVENTS2HISTOGRAM



#ifdef DEBUG
#include "journal/debug.h"
#endif

namespace ARCS_EventData{

  struct Event;
  
  template <typename Histogrammer, typename EventIterator>
  void events2histogram
  (const EventIterator events_begin, size_t N, Histogrammer & her )
  {
#ifdef DEBUG
    journal::debug_t debug("events2histogram");
#endif

    for (size_t i=0; i< N; i++ ) {
#ifdef DEBUG
      debug << journal::at(__HERE__)
	    << "event # " << i 
	    << journal::endl;
#endif
      her( *(events_begin+i) );
    }
    
#ifdef DEBUG
    debug << journal::at(__HERE__)
	  << "done histogramming."
	  << journal::endl;
#endif
  }

}


#endif // H_ARCSEVENTDATA_EVENTS2HISTOGRAM


// version
// $Id$

// End of file 
