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


#ifndef WRAP_READEVENTS_H
#define WRAP_READEVENTS_H


#include "Python.h"


namespace wrap_arcseventdata
{

  // readevents
  extern char readevents__name__[];
  extern char readevents__doc__[];
  extern "C"
  PyObject * readevents(PyObject *, PyObject *args);

} // wrap_arcseventdata::

#endif // WRAP_READEVENTS_H



// version
// $Id$

// End of file
