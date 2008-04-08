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


template <typename FLT, int TypeCode>
void test()
{
  PyObject * po = PyArray_Arange(10.0, 20., 1., TypeCode);
  
  std::cout << "po=" << po << std::endl;

  FLT a5 = * (FLT *) (PyArray_GETPTR1 (po, 5) );

  std::cout << "po[5]=" << a5 << std::endl;

  FLT * data = (FLT *) PyArray_BYTES( po );
  size_t size = PyArray_Size( po );
  
  std::cout << "array = " ;
  for (size_t i=0; i<size; i++)
    std::cout << data[i];
  std::cout << std::endl;

  using namespace reductionmod;

  typedef Array1DIterator< FLT > Iterator;

  //ctors
  //ctor from array object and copy ctor
  Iterator begin (po), end = begin + PyArray_Size(po);
  //ctor from PyArrayIterObject
  PyArrayIterObject *arrIt = (PyArrayIterObject*)PyArray_IterNew( po );
  Iterator it1(arrIt);// assert (it1 == begin);

  // operator +/-
  begin + 3;
  end - 3;
  std::cout << (end-begin) << "," << size << std::endl;
  assert( end - begin == size );

  // operator ++
  for (Iterator it = begin; it<end; ++it) {
    FLT expected = (it-begin) + *begin ;
    assert ( (*it - expected)/expected < 1.e-7 );
  }
  Iterator it2 = begin;
  Iterator it3 = it2++;
  assert (it3==it2-1);
  it3 = ++it2;
  assert (it3==it2);
  
  // operator --
  it3 = --it2;
  assert( it3==it2);
  it3 = it2--;
  assert (it3==it2+1);

  // operator *
  assert( *begin - 10.0 < 1.e-7 );
  *begin = 0.0;
  *begin = 10.0;    
  
  // ==
  assert( begin + size == end );

  // !=
  assert( begin != end );

  // <
  assert( begin < begin+1 );

  // >
  assert( begin+1 > begin );

  // <<
  std::cout 
    << "begin = " << begin << "," 
    << "end = " << end << "," 
    << std::endl;

  // index < 0
  Iterator it5 = begin - 1;
  assert (begin - it5 == 1);
  try {
    *it5;
    throw;
  }
  catch (index_out_of_bound &err) {
    std::cout << "Good. caught error" << std::endl;
  }
  Iterator it6 = end-1, it7 = it6-size;
  std::cout 
    << "it6 = " << it6 << std::endl
    << "it7 = " << it7 << std::endl
    << std::endl;
  assert (it6-it7==size);

  // ReverseIterator
  typedef DANSE::ReverseIterator<Iterator, FLT> RIterator;
  RIterator rit1 (begin), rit2 (end), rit3(end-1), rit4 = rit3+(end-begin);
  std::cout 
    << "rit1 = " << rit1 << std::endl
    << "rit2 = " << rit2 << std::endl
    << "rit3 = " << rit3 << std::endl
    << "rit4 = " << rit4 << std::endl
    ;
  assert (rit4-rit3==size);

}


int main()
{
  Py_Initialize();
  PyRun_SimpleString("from time import time,ctime\n"
                     "print 'Today is',ctime(time())\n");

  _import_numpy();
  test<npy_float, NPY_FLOAT>();
  test<npy_double, NPY_DOUBLE>();
  test<double, NPY_DOUBLE>();

  Py_Finalize();
  return 0;
}


// version
// $Id$

// End of file 
