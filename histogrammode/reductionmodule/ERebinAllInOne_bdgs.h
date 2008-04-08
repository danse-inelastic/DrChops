// Timothy M. Kelley Copyright (c) 2005 All rights reserved
#ifndef EREBINALLINONE_BDGS_H
#define EREBINALLINONE_BDGS_H

#ifndef PYTHON_INCLUDED
#define PYHTON_INCLUDED
#include <Python.h>
#endif

namespace reductionmod
{
  extern const int ERebinAllInOne__magicNumber__;
  
  extern char ERebinAllInOne_ctor__name__[];
  extern char ERebinAllInOne_ctor__doc__[];
  extern "C"
    PyObject * ERebinAllInOne_ctor(PyObject *, PyObject *args);
  
  extern char ERebinAllInOne_call__name__[];
  extern char ERebinAllInOne_call__doc__[];
  extern "C"
    PyObject * ERebinAllInOne_call(PyObject *, PyObject *args);
  
} // reductionmod::

#endif



// version
// $Id: ERebinAllInOne_bdgs.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
