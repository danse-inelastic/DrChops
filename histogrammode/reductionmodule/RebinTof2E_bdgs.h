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


#ifndef REDUCTION_REBINTOF2E_BDGS_H
#define REDUCTION_REBINTOF2E_BDGS_H


#include "Python.h"


namespace reductionmod
{
  
  // constructor
  extern char RebinTof2E__name__[];
  extern char RebinTof2E__doc__[];
  extern "C"
  PyObject * RebinTof2E(PyObject *, PyObject *args);
  
  
  // __call__
  extern char RebinTof2ECall_numpyarray__name__[];
  extern char RebinTof2ECall_numpyarray__doc__[];
  extern "C"
  PyObject * RebinTof2ECall_numpyarray(PyObject *, PyObject *args);
  
} // reductionmod::

#endif // REDUCTION_REBINTOF2E_BDGS_H



// version
// $Id: RebinTof2E_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
