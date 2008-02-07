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

#include <sstream>
#include <iostream>

#include "wrap_readevents.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/EventsReader.h"

#include "utils.h"


namespace wrap_arcseventdata
{
  
  using namespace ARCS_EventData;
  
  // 
  char readevents__name__[] = "readevents";
  char readevents__doc__[] = "readevents\n" \
"readevents( arcs_event_data_pre_nexus_filename, nevents, start = 0 )\n"\
" nevents: number of events\n"\
" start: starting point of reading in terms of number of events\n"
;
  
  PyObject * readevents(PyObject *, PyObject *args)
  {
    char *filename;
    long nevents, start = 0;

    std::ostringstream oss;
    
    int ok = PyArg_ParseTuple(args, "sl|l", &filename, &nevents, &start); 

    if (!ok) return 0;

    Event * pevents ;
    try {
      EventsReader reader( filename );
      pevents= reader.read( start, start + nevents );
    }
    catch (...) {
      oss << "Unable to read events from " << filename;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }
    
    if (pevents == 0) {
      oss << "Unable to read events from " << filename;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }
    
    return PyCObject_FromVoidPtr( pevents, deleteArrayPtr<Event> );
  }
  
} // wrap_events2EvenlySpacedIx::



// version
// $Id$

// End of file
