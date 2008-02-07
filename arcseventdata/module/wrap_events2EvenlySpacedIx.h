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


#ifndef WRAP_EVENTS2EVENLYSPACEDIX_H
#define WRAP_EVENTS2EVENLYSPACEDIX_H


#include "Python.h"


namespace wrap_arcseventdata
{

  // events2Ipix
  extern char events2Ipix_numpyarray__name__[];
  extern char events2Ipix_numpyarray__doc__[];
  extern "C"
  PyObject * events2Ipix_numpyarray(PyObject *, PyObject *args);

  // events2Itof
  extern char events2Itof_numpyarray__name__[];
  extern char events2Itof_numpyarray__doc__[];
  extern "C"
  PyObject * events2Itof_numpyarray(PyObject *, PyObject *args);

  // events2Idspacing
  extern char events2Idspacing_numpyarray__name__[];
  extern char events2Idspacing_numpyarray__doc__[];
  extern "C"
  PyObject * events2Idspacing_numpyarray(PyObject *, PyObject *args);

} // wrap_arcseventdata::

#endif // WRAP_EVENTS2EVENLYSPACEDIX_H



// version
// $Id$

// End of file
