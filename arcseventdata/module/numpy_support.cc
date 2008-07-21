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
#include <Python.h>
#include "numpy_support.h"

namespace reductionmod{

  bool checkDataType( PyObject * obj, const char * name, int typecode )
  {
    std::ostringstream oss;

    if (!PyArray_Check(obj)) {
      oss << name <<  " is not a numpy array" << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 1;
    }
    if (PyArray_TYPE( obj ) != typecode ) {
      oss << "In file " << __FILE__ << ", line " << __LINE__ << ", "
	  << name 
	  << " must be a numpy array of type " << typecode << ", "
	  << " but its type code actually is " << PyArray_TYPE( obj ) << "."
	  << std::endl;
      PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
      return 1;
    }
    return 0;
  }

} // reductionmod::

// version
// $Id$

// End of file 
