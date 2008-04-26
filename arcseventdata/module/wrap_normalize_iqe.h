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


#ifndef WRAP_NORMALIZE_IQE_H
#define WRAP_NORMALIZE_IQE_H


#include "Python.h"


namespace wrap_arcseventdata
{

  // calcSolidAngleQE
  extern char calcSolidAngleQE_numpyarray__name__[];
  extern char calcSolidAngleQE_numpyarray__doc__[];
  extern "C"
  PyObject * calcSolidAngleQE_numpyarray(PyObject *, PyObject *args);

} // wrap_arcseventdata::

#endif // WRAP_NORMALIZE_IQE_H



// version
// $Id$

// End of file
