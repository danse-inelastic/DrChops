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

#include <sstream>
#include <iostream>

#include "utils.h"
#include "numpy_support.h"
#include "Zt2Zxy_bdgs.h"

#include "drchops/Zt2Zxy.h"


namespace reductionmod
{

  typedef Array1DIterator<npy_double> DblArrIt;
  //typedef Array1DIterator<npy_bool> BoolArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  using DANSE::Reduction::utils::deleteHeapObj;

  namespace Zt2Zxy_impl {

    template <typename DataIterator, int datatypecode,
	      typename MaskIterator, int masktypecode,
	      typename FLT>
    PyObject * call_numpyarray
    (PyObject *pyxt, PyObject *pyyt, PyObject *pyzt,
     PyObject *pymaskt, 
     PyObject *pyxbb, PyObject *pyybb, 
     PyObject *pyoutzxy
     )

    {
      if (checkDataType(pyxt, "xt", datatypecode)) return 0;
      if (checkDataType(pyyt, "yt", datatypecode)) return 0;
      if (checkDataType(pyzt, "zt", datatypecode)) return 0;
      if (checkDataType(pyxbb, "xbb", datatypecode)) return 0;
      if (checkDataType(pyybb, "ybb", datatypecode)) return 0;
      if (checkDataType(pyoutzxy, "zxy", datatypecode)) return 0;
      if (checkDataType(pymaskt, "maskarr",  masktypecode)) return 0;
      
      std::ostringstream oss;

      size_t nxbbs = PyArray_Size( pyxbb ), 
	nybbs = PyArray_Size( pyybb ), 
	zxySize = PyArray_Size( pyoutzxy );
    
      if (zxySize == 0 || zxySize!=(nxbbs-1)*(nybbs-1)) {
	oss << "output array zxy: size=" << zxySize << ", "
	    << "no. of x bins: " << nxbbs-1 << ", "
	    << "no. of y bins: " << nybbs-1 << ", "
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      size_t ntx = PyArray_Size(pyxt), nty=PyArray_Size(pyyt), ntz=PyArray_Size(pyzt),
	ntmask = PyArray_Size(pymaskt);
      if (ntx!=nty || ntx!=ntz || ntx!=ntmask) {
	oss << "Size mismatch:"
	    << "mask(t) size: " << ntmask
	    << "x(t) size: " << ntx
	    << "y(t) size: " << nty
	    << "z(t) size: " << ntz
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      size_t nt = ntx;

      
      DataIterator x_begin (pyxt), y_begin (pyyt), z_begin (pyzt), 
	outxbb_begin(pyxbb), outxbb_end=outxbb_begin+nxbbs,
	outybb_begin(pyybb), outybb_end=outybb_begin+nybbs,
	outz_begin(pyoutzxy)
	;
      
      MaskIterator mask_begin( pymaskt );

      using namespace DANSE::Reduction;
      Zt2Zxy
	<FLT, FLT, FLT,
	DataIterator, DataIterator, DataIterator, MaskIterator,
	DataIterator, DataIterator, DataIterator>
	(x_begin, y_begin, z_begin,
	 mask_begin,
	 nt,
	 outxbb_begin, outxbb_end,
	 outybb_begin, outybb_end,
	 outz_begin
	 );
      
      return Py_None;
    }
    
  }

  // constructor
  char Zt2Zxy_numpyarray__name__[] = "Zt2Zxy_numpyarray";
  char Zt2Zxy_numpyarray__doc__[] = "Zt2Zxy_numpyarray\n"\
  "Zt2Zxy( xt, yt, zt, maskt, outxbb, outybb, outzxy) \n"\
  "xt: array of x values for x(t)\n" \
  "yt: array of y values for y(t)\n" \
  "zt: array of z values for z(t)\n" \
  "maskt: array of mask values for mask(t)\n" \
  "outxbb: x bin boundaries for the output z[x,y]\n" \
  "outybb: y bin boundaries for the output z[x,y]\n" \
  "outzxy: array of z to store the output z[x,y]\n" \
  ;

  PyObject * Zt2Zxy_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pyxt, *pyyt, *pyzt, *pymaskt, *pyoutxbb, *pyoutybb, *pyoutzxy;

    int ok = PyArg_ParseTuple
      (args, "OOOOOOO", 
       &pyxt, &pyyt, &pyzt, &pymaskt,
       &pyoutxbb, &pyoutybb, &pyoutzxy
       );

    if (!ok) return 0;

    return Zt2Zxy_impl::call_numpyarray
      <DblArrIt, NPY_DOUBLE,
      IntArrIt, NPY_INT,
      npy_double>
      (pyxt, pyyt, pyzt, pymaskt, pyoutxbb, pyoutybb, pyoutzxy
       );

  }
    
} // reductionmod::



// version
// $Id$

// End of file
