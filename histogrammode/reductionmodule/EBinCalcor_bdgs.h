// Timothy M. Kelley Copyright (c) 2005 All rights reserved
#ifndef EBINCALCOR_BDGS_H
#define EBINCALCOR_BDGS_H

#ifndef PYTHON_INCLUDED
#define PYTHON_INCLUDED
#include "Python.h"
#endif

namespace reductionmod
{
    // magic number for T wrapper
    extern int EBinCalcor__magicNumber__;

    extern char EBinCalcor__name__[];
    extern char EBinCalcor__doc__[];
    extern "C"
    PyObject * EBinCalcor(PyObject *, PyObject *args);
    
    extern char EBinCalcorCall__name__[];
    extern char EBinCalcorCall__doc__[];
    extern "C"
    PyObject * EBinCalcorCall(PyObject *, PyObject *args);

} // reductionmod::

#endif



// version
// $Id: EBinCalcor_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
