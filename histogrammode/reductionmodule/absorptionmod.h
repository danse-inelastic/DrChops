// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2003-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef ABSORPTIONMOD_H
#define ABSORPTIONMOD_H

#ifndef PYTHON_INCLUDED
#define PYHTON_INCLUDED
#include <Python.h>
#endif

namespace reductionmod
{
  extern int vanPlateXmission__magicNumber__;
  
  extern char vanPlateXmission_ctor__name__[];
  extern char vanPlateXmission_ctor__doc__[];
  extern "C"
  PyObject * vanPlateXmission_ctor(PyObject *, PyObject *args);
  
  extern char vanPlateXmission_call__name__[];
  extern char vanPlateXmission_call__doc__[];
  extern "C"
  PyObject * vanPlateXmission_call(PyObject *, PyObject *args);
  
} // reductionmod::

#endif


// version
// $Id: absorptionmod.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
