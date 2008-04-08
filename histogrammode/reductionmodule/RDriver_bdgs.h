// Timothy M. Kelley Copyright (c) 2005 All rights reserved
#ifndef RDRIVER_BDGS_H
#define RDRIVER_BDGS_H

#include "Python.h"

namespace reductionmod
{
  extern int RDriver__magicNumber__;
  
  extern char RDriver__name__[];
  extern char RDriver__doc__[];
  extern "C"
  PyObject * RDriver(PyObject *, PyObject *args);
  
  extern char RDriver_call__name__[];
  extern char RDriver_call__doc__[];
  extern "C"
  PyObject * RDriver_call(PyObject *, PyObject *args);
  
  extern char RDriver_norms__name__[];
  extern char RDriver_norms__doc__[];
  extern "C"
  PyObject * RDriver_norms(PyObject *, PyObject *args);
  
} // reductionmod::

#endif


// version
// $Id: RDriver_bdgs.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
