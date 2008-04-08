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

#include "reduction/utils.h"
#include "numpy_support.h"
#include "RebinTof2E_batch_bdgs.h"

#include "reduction/RebinTof2E_batch.h"


namespace reductionmod
{

  typedef Array1DIterator<npy_double> DblArrIt;
  //typedef Array1DIterator<npy_bool> BoolArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  using DANSE::Reduction::utils::deleteHeapObj;

  namespace RebinTof2E_batch_impl {

    template <typename DataIterator, int datatypecode,
	      typename MaskIterator, int masktypecode,
	      typename FLT>
    PyObject * call_Istartof2IE_numpyarray
    (PyObject *pytofbb, PyObject *pyItof, PyObject *pyItoferr2,
     PyObject *pyebb, PyObject *pyI_E, PyObject *pyI_Eerr2, 
     PyObject *pydistarr, PyObject *pymaskarr, 
     PyObject *pytmpE, PyObject *pytmpI )
    {
      if (checkDataType(pytofbb, "tofbb", datatypecode)) return 0;
      if (checkDataType(pyItof, "Itof", datatypecode)) return 0;
      if (checkDataType(pyItoferr2, "Itoferr2", datatypecode)) return 0;
      if (checkDataType(pyebb, "ebb",  datatypecode)) return 0;
      if (checkDataType(pyI_E, "I_E",  datatypecode)) return 0;
      if (checkDataType(pyI_Eerr2, "I_Eerr2",  datatypecode)) return 0;
      if (checkDataType(pydistarr, "distarr",  datatypecode)) return 0;
      if (checkDataType(pymaskarr, "maskarr",  masktypecode)) return 0;
      if (checkDataType(pytmpE, "tmpE",  datatypecode)) return 0;
      if (checkDataType(pytmpI, "tmpI",  datatypecode)) return 0;
      
      std::ostringstream oss;

      size_t ntofbbs = PyArray_Size( pytofbb ), totsize = PyArray_Size( pyItof ),
	totsize1 = PyArray_Size( pyItoferr2 );
    
      if (totsize != totsize1 || totsize == 0) {
	oss << "Size mismatch: "
	    << "cnts[*,tof] : size = " << totsize << ", "
	    << "errs[*,tof] : size = " << totsize1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      
      size_t npixels = totsize/(ntofbbs-1);
      if (totsize != npixels * (ntofbbs-1) ) {
	oss << "Invalid shape: "
	    << "ntof * npixels != totsize." << std::endl
	    << ntofbbs-1 << " * " << npixels << " != " << totsize 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t nebbs = PyArray_Size( pyebb ),
	nEbins = PyArray_Size( pyI_E ), nEbins1 = PyArray_Size( pyI_Eerr2 );

      if (nEbins != nEbins1 || nEbins==0 ) {
	oss << "Size mismatch: "
	    << "S[Q,E] : size = " << nEbins << ", "
	    << "S_err2[Q,E] : size = " << nEbins1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      if (nEbins != nebbs-1 ) {
	oss << "Invalid array sizes: "
	    << "nebbs-1 !=  nEbins." << std::endl
	    << nebbs-1 << " != " << nEbins 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t masksize = PyArray_Size( pymaskarr ), 
	distsize = PyArray_Size( pydistarr );
      if (npixels != masksize || npixels != distsize || npixels == 0) {
	oss << "Size mismatch: "
	    << "npixels = " << npixels << ","
	    << "masksize = " << masksize << ","
	    << "distsize = " << distsize << ","
	  ;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t tmpEsize = PyArray_Size( pytmpE ), tmpIsize = PyArray_Size( pytmpI );
      if (ntofbbs != tmpEsize || tmpEsize == 0) {
	oss << "Size mismatch: "
	    << "tmpE array length " << tmpEsize << " should be the same as "
	    << "number of tof bin boundaries " << ntofbbs;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      if (nebbs-1 != tmpIsize || tmpIsize == 0 ) {
	oss << "Size mismatch: "
	    << "tmpI array length " << tmpIsize << " should be one less than "
	    << "number of E bin boundaries " << nebbs;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      DataIterator tofbb_begin (pytofbb), tofbb_end = tofbb_begin + ntofbbs,
	Itof_begin(pyItof), Itoferr2_begin( pyItoferr2 ),
	ebb_begin( pyebb ), ebb_end = ebb_begin + PyArray_Size( pyebb ),
	I_E_begin(pyI_E), I_Eerr2_begin( pyI_Eerr2 ), 
	dist_begin( pydistarr ),
	tmpE_begin( pytmpE ), tmpI_begin( pytmpI );
      
      MaskIterator mask_begin( pymaskarr );

      //    std::cout << "ei=" << ei<< ", mod2sample =" << mod2sample << std::endl;
      DANSE::Reduction::Istartof2IE
	<FLT, DataIterator, DataIterator, DataIterator, DataIterator, 
	DataIterator, MaskIterator >
	(tofbb_begin, tofbb_end, 
	 Itof_begin, Itoferr2_begin,
	 ebb_begin, ebb_end,
	 I_E_begin, I_Eerr2_begin, 
	 dist_begin, mask_begin, 
	 npixels,
	 tmpE_begin, tmpI_begin );
      
      return Py_None;
    }
    
  }



  char Istartof2IE_numpyarray__name__[] = "Istartof2IE_numpyarray";
  char Istartof2IE_numpyarray__doc__[] = "Istartof2IE_numpyarray\n"\
  "Istartof2IE( tofbb, Itof, Itoferr2, \n"\
  "             ebb, I_E, I_Eerr2, \n"\
  "             distarr, maskarr, \n"\
  "             tmpE, tmpI)\n"\
  "tofbb: tof bin boundaries\n"\
  "Itof: counts[*,tof] matrix\n"   \
  "Itoferr2: counts_err2[*,tof] matrix\n"   \
  "ebb: e bin boundaries\n" \
  "I_E: S[phi,E] matrix \n" \
  "I_Eerr2: I_Eerr2[phi,E] matrix\n"\
  "distarr: distance[*] array\n"\
  "maskarr: mask[*] array\n"\
  "tmpE: a temporary array. length = len(tofbb) \n"	\
  "tmpI: a temporary array. length = len(ebb)-1 \n"  \
  ;

  PyObject * Istartof2IE_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pytofbb, *pyItof, *pyItoferr2,
      *pyebb, *pyI_E, *pyI_Eerr2, 
      *pydistarr, *pymaskarr, 
      *pytmpE, *pytmpI;

    int ok = PyArg_ParseTuple
      (args, "OOOOOOOOOO", 
       &pytofbb, &pyItof, &pyItoferr2,
       &pyebb, &pyI_E, &pyI_Eerr2, 
       &pydistarr, &pymaskarr,
       &pytmpE, &pytmpI);

    if (!ok) return 0;

    return RebinTof2E_batch_impl::call_Istartof2IE_numpyarray
      <DblArrIt, NPY_DOUBLE,
      IntArrIt, NPY_INT,
      npy_double>
      (pytofbb, pyItof, pyItoferr2,
       pyebb, pyI_E, pyI_Eerr2, 
       pydistarr, pymaskarr, 
       pytmpE, pytmpI);
  }
    
} // reductionmod::



// version
// $Id: RebinTof2E_batch_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
