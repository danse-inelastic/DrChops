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


#ifndef WRAP_EVENTS2EVENLYSPACEDIXY_H
#define WRAP_EVENTS2EVENLYSPACEDIXY_H


#include "Python.h"


namespace wrap_arcseventdata
{

  // events2IpixE
  extern char events2IpixE_numpyarray__name__[];
  extern char events2IpixE_numpyarray__doc__[];
  extern "C"
  PyObject * events2IpixE_numpyarray(PyObject *, PyObject *args);

  // events2IQE
  extern char events2IQE_numpyarray__name__[];
  extern char events2IQE_numpyarray__doc__[];
  extern "C"
  PyObject * events2IQE_numpyarray(PyObject *, PyObject *args);

  // events2Ipixtof
  extern char events2Ipixtof_numpyarray__name__[];
  extern char events2Ipixtof_numpyarray__doc__[];
  extern "C"
  PyObject * events2Ipixtof_numpyarray(PyObject *, PyObject *args);

  // events2Ipixd
  extern char events2Ipixd_numpyarray__name__[];
  extern char events2Ipixd_numpyarray__doc__[];
  extern "C"
  PyObject * events2Ipixd_numpyarray(PyObject *, PyObject *args);

  // events2IpixEi
  extern char events2IpixEi_numpyarray__name__[];
  extern char events2IpixEi_numpyarray__doc__[];
  extern "C"
  PyObject * events2IpixEi_numpyarray(PyObject *, PyObject *args);

  // events2IpixL
  extern char events2IpixL_numpyarray__name__[];
  extern char events2IpixL_numpyarray__doc__[];
  extern "C"
  PyObject * events2IpixL_numpyarray(PyObject *, PyObject *args);

} // wrap_arcseventdata::

#endif // WRAP_EVENTS2EVENLYSPACEDIXY_H



// version
// $Id$

// End of file
