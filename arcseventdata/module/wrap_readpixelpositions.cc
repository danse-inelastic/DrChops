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

#include "wrap_readpixelpositions.h"

#include "arcseventdata/Event.h"
#include "arcseventdata/readPixelPositions.h"

#include "utils.h"


namespace wrap_arcseventdata
{
  
  using namespace ARCS_EventData;
  
  // 
  char readpixelpositions__name__[] = "readpixelpositions";
  char readpixelpositions__doc__[] = "readpixelpositions\n" \
"readpixelpositions( filename, npacks, ndetsperpack, npixelsperdet )"
;
  
  PyObject * readpixelpositions(PyObject *, PyObject *args)
  {
    char *filename;
    int npacks=115, ndetsperpack = 8, npixelsperdet = 128;

    std::ostringstream oss;
    
    int ok = PyArg_ParseTuple(args, "s|iii", &filename, &npacks, &ndetsperpack, &npixelsperdet); 

    if (!ok) return 0;

    double * ptr;

    try {
      ptr = readPixelPositions( filename, npacks, ndetsperpack, npixelsperdet );
    }
    catch(...) {
      oss << "Unable to read pixel-positions from " << filename;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }

    if (ptr == 0) {
      oss << "Unable to read pixel-positions from " << filename;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 0;
    }
    
    return PyCObject_FromVoidPtr( ptr, deleteArrayPtr<double> );
  }
  
} // wrap_arcseventdata::



// version
// $Id$

// End of file
