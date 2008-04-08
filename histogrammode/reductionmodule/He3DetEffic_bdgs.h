// Timothy M. Kelley Copyright (c) 2005 All rights reserved
#ifndef HE3DETEFFIC_BDGS_H
#define HE3DETEFFIC_BDGS_H

#ifndef PYTHON_INCLUDED
#define PYHTON_INCLUDED
#include <Python.h>
#endif

namespace reductionmod
{
  extern char He3DetEffic__name__[];
  extern char He3DetEffic__doc__[];
  extern "C"
  PyObject * He3DetEffic(PyObject *, PyObject *args);
  
  extern char He3DetEfficExecSingle__name__[];
  extern char He3DetEfficExecSingle__doc__[];
  extern "C"
  PyObject * He3DetEfficExecSingle(PyObject *, PyObject *args);
  
  extern char He3DetEffic_classID__name__[];
  extern char He3DetEffic_classID__doc__[];
  extern "C"
  PyObject * He3DetEffic_classID(PyObject *, PyObject *args);
  
  extern char He3DetEfficExecVector__name__[];
  extern char He3DetEfficExecVector__doc__[];
  extern "C"
  PyObject * He3DetEfficExecVector(PyObject *, PyObject *args);
  
} // reductionmod::


#endif



// version
// $Id: He3DetEffic_bdgs.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
