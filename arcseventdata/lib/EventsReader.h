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


#ifndef H_ARCS_EVENTDATA_READEVENT
#define H_ARCS_EVENTDATA_READEVENT

#include <fstream>
#include "Event.h"

namespace ARCS_EventData{

  class EventsReader {

  public:
    
    // meta methods
    EventsReader( const char * filename );
    ~EventsReader();

    // methods
    /// read n events from start of the event file
    Event * read( size_t n );
    /// read events[n1:n2] from file
    Event * read( size_t n1, size_t n2 );

  private:
    // data
    std::ifstream *m_f;
  };
}

#endif


// version
// $Id$

// End of file 
