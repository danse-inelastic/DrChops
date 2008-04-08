// Timothy M. Kelley Copyright (c) 2005 All rights reserved
#ifndef QBINCALCOR_BDGS_H
#define QBINCALCOR_BDGS_H

#include "Python.h"

namespace reductionmod
{
  extern int QBinCalcor__magicNumber__;
  
  extern char QBinCalcor_ctor__name__[];
  extern char QBinCalcor_ctor__doc__[];
  extern "C"
  PyObject * QBinCalcor_ctor(PyObject *, PyObject *args);
  
  extern char QBinCalcorCall__name__[];
  extern char QBinCalcorCall__doc__[];
  extern "C"
  PyObject * QBinCalcorCall(PyObject *, PyObject *args);
  
} // reductionmod

#endif



// version
// $Id: QBinCalcor_bdgs.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
