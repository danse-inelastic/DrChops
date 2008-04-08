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

#include <cassert>
#include <cmath>
#include <iostream>
#include <sstream>
#include <Python.h>

#define STANDALONE_USE_OF_NUMPY_SUPPORT
#include "../../reductionmodule/numpy_support.h"
#include "../../libreduction/ReverseIterator.h"


void _import_numpy()
{
 import_array();
}


/// test operator=
template <typename FLT, int TypeCode>
void test()
{
  PyObject * po = PyArray_Arange(10.0, 20., 1., TypeCode);
  
  std::cout << "po=" << po << std::endl;

  using namespace reductionmod;

  typedef Array1DIterator< FLT > Iterator;

  //ctors
  //ctor from array object and copy ctor
  Iterator begin (po);
  
  Iterator a;
  a = begin;

  std::cout <<  a << std::endl;
  std::cout <<  ++a << std::endl;
  std::cout <<  begin << std::endl;
}


int main()
{
  Py_Initialize();
  PyRun_SimpleString("from time import time,ctime\n"
                     "print 'Today is',ctime(time())\n");

  _import_numpy();
  test<npy_double, NPY_DOUBLE>();

  Py_Finalize();
  return 0;
}


// version
// $Id$

// End of file 
