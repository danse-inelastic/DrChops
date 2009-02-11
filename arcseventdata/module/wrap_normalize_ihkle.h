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


#ifndef WRAP_NORMALIZE_IHKLE_H
#define WRAP_NORMALIZE_IHKLE_H


#include "Python.h"


namespace wrap_arcseventdata
{

  // calcSolidAngleHKLE
  extern char calcSolidAngleHKLE_numpyarray__name__[];
  extern char calcSolidAngleHKLE_numpyarray__doc__[];
  extern "C"
  PyObject * calcSolidAngleHKLE_numpyarray(PyObject *, PyObject *args);

} // wrap_arcseventdata::

#endif // WRAP_NORMALIZE_IHKLE_H



// version
// $Id$

// End of file
