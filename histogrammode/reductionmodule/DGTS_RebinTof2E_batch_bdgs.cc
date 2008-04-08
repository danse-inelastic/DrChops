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
#include "DGTS_RebinTof2E_batch_bdgs.h"

#include "reduction/DGTS_RebinTof2E_batch.h"
#include "reduction/He3EfficiencyCorrection.h"


namespace reductionmod
{

  typedef Array1DIterator<npy_double> DblArrIt;
  //typedef Array1DIterator<npy_bool> BoolArrIt;
  typedef Array1DIterator<npy_int> IntArrIt;

  using DANSE::Reduction::utils::deleteHeapObj;

  namespace DGTS_RebinTof2E_batch_impl {

    template <typename DataIterator, int datatypecode,
	      typename MaskIterator, int masktypecode,
	      typename FLT>
    PyObject * call_numpyarray
    (PyObject *pytofbb, PyObject *pycntsmat, PyObject *pyerr2mat,
     PyObject *pyphibb, PyObject *pyebb, 
     PyObject *pySmat, PyObject *pySerr2, PyObject *pyintsa,
     PyObject *pymaskarr, PyObject *pyphiarr, PyObject *pysaarr,
     PyObject *pydistarr, 
     PyObject *pyradiusarr, PyObject *pypressurearr,
     PyObject *pytmpE, PyObject *pytmpI, 
     const FLT & ei, const FLT & mod2sample )
    {
      if (checkDataType(pytofbb, "tofbb", datatypecode)) return 0;
      if (checkDataType(pycntsmat, "cntsmat", datatypecode)) return 0;
      if (checkDataType(pyerr2mat, "err2mat", datatypecode)) return 0;
      if (checkDataType(pyphibb, "phibb",  datatypecode)) return 0;
      if (checkDataType(pyebb, "ebb",  datatypecode)) return 0;
      if (checkDataType(pySmat, "Smat",  datatypecode)) return 0;
      if (checkDataType(pySerr2, "Serr2",  datatypecode)) return 0;
      if (checkDataType(pyintsa, "intsa",  datatypecode)) return 0;
      if (checkDataType(pymaskarr, "maskarr",  masktypecode)) return 0;
      if (checkDataType(pyphiarr, "phiarr",  datatypecode)) return 0;
      if (checkDataType(pysaarr, "saarr",  datatypecode)) return 0;
      if (checkDataType(pydistarr, "distarr",  datatypecode)) return 0;
      if (checkDataType(pyradiusarr, "radiusarr",  datatypecode)) return 0;
      if (checkDataType(pypressurearr, "pressurearr",  datatypecode)) return 0;
      if (checkDataType(pytmpE, "tmpE",  datatypecode)) return 0;
      if (checkDataType(pytmpI, "tmpI",  datatypecode)) return 0;
      
      std::ostringstream oss;

      size_t ntofbbs = PyArray_Size( pytofbb ), totsize = PyArray_Size( pycntsmat ),
	totsize1 = PyArray_Size( pyerr2mat );
    
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

      size_t nphibbs = PyArray_Size( pyphibb ), nebbs = PyArray_Size( pyebb ),
	nS = PyArray_Size( pySmat ), nS1 = PyArray_Size( pySerr2 );

      if (nS != nS1 || nS==0 ) {
	oss << "Size mismatch: "
	    << "S[Q,E] : size = " << nS << ", "
	    << "S_err2[Q,E] : size = " << nS1 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      if (nS != (nphibbs-1) * (nebbs-1) ) {
	oss << "Invalid shape: "
	    << "nphi * ne !=  size(S)." << std::endl
	    << nphibbs-1 << " * " << nebbs-1 << " != " << nS 
	    << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }
      size_t nintsa = PyArray_Size( pyintsa );
      if (nintsa != nphibbs-1) {
	oss << "Integrated solid angle: invalid size: " << nintsa
	    << ", should be " << nphibbs-1 << std::endl;
	PyErr_SetString( PyExc_ValueError, oss.str().c_str() );
	return 0;
      }

      size_t masksize = PyArray_Size( pymaskarr ), 
	phisize = PyArray_Size( pyphiarr ),
	sasize = PyArray_Size( pysaarr ),
	distsize = PyArray_Size( pydistarr ),
	radiussize = PyArray_Size( pyradiusarr ),
	pressuresize = PyArray_Size( pypressurearr )
	;
      if (npixels != masksize || npixels != phisize || npixels!=sasize
	  || npixels != distsize || npixels != radiussize || npixels != pressuresize
	  || npixels == 0) {
	oss << "Size mismatch: "
	    << "npixels = " << npixels << ","
	    << "masksize = " << masksize << ","
	    << "phisize = " << phisize << ","
	    << "sasize = " << sasize << ","
	    << "distsize = " << distsize << ","
	    << "radiussize = " << radiussize << ","
	    << "pressuresize = " << pressuresize << ","
	    << std::endl;
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

      DataIterator tofbb_begin (pytofbb), tofbb_end = tofbb_begin + PyArray_Size(pytofbb),
	cntsmat_begin(pycntsmat), err2mat_begin( pyerr2mat ),
	phibb_begin( pyphibb ), phibb_end = phibb_begin + PyArray_Size( pyphibb ),
	ebb_begin( pyebb ), ebb_end = ebb_begin + PyArray_Size( pyebb ),
	S_begin(pySmat), Serr2_begin( pySerr2 ), intsa_begin( pyintsa ),
	phi_begin( pyphiarr ), sa_begin( pysaarr ), dist_begin( pydistarr ),
	radius_begin( pyradiusarr ), pressure_begin( pypressurearr ),
	tmpE_begin( pytmpE ), tmpI_begin( pytmpI );
      
      MaskIterator mask_begin( pymaskarr );

      //    std::cout << "ei=" << ei<< ", mod2sample =" << mod2sample << std::endl;
      using namespace DANSE::Reduction;
      DGTS_RebinTof2E_batch
	<FLT, DataIterator, DataIterator, DataIterator, DataIterator, MaskIterator,
	He3EfficiencyCorrection<FLT, typename std::vector<FLT>::iterator, DataIterator >
	>
	(tofbb_begin, tofbb_end, 
	 cntsmat_begin, err2mat_begin,
	 phibb_begin, phibb_end,
	 ebb_begin, ebb_end,
	 S_begin, Serr2_begin, intsa_begin,
	 ei, mod2sample,
	 mask_begin, phi_begin, sa_begin, dist_begin,
	 radius_begin, pressure_begin,
	 npixels,
	 tmpE_begin, tmpI_begin );
      
      return Py_None;
    }
    
  }

  // constructor
  char DGTS_RebinTof2E_batch_numpyarray__name__[] = "DGTS_RebinTof2E_batch_numpyarray";
  char DGTS_RebinTof2E_batch_numpyarray__doc__[] = "DGTS_RebinTof2E_batch_numpyarray\n"\
  "DGTS_RebinTof2E_batch( tofbb, cntsmat, err2mat, \n"\
  "                       phibb, ebb, Smat, Serr2, \n"\
  "                       ei, mod2sample, \n"\
  "                       maskarr, phiarr, distarr, \n"\
  "                       radiusarr, pressurearr, \n"\
  "                       tmpE, tmpI)\n"\
  "tofbb: tof bin boundaries\n"\
  "cntsmat: counts[*,tof] matrix\n"   \
  "err2mat: counts_err2[*,tof] matrix\n"   \
  "phibb: phi bin boundaries\n" \
  "ebb: e bin boundaries\n" \
  "Smat: S[phi,E] matrix \n" \
  "Serr2: Serr2[phi,E] matrix\n"\
  "integrated_solidangle: integrated_solidangle[phi]\n"
  "ei: incident energy (meV)\n"\
  "mod2sample: moderator-to-sample distance (mm)\n"\
  "maskarr: mask[*] array\n"\
  "phiarr: phi[*] array\n"\
  "solidanglearr: solidangle[*] array\n"\
  "distarr: distance[*] array\n"\
  "radiusarr: radius[*] array\n"\
  "pressurearr: pressure[*] array\n"\
  "tmpE: a temporary array. length = len(tofbb) \n"	\
  "tmpI: a temporary array. length = len(ebb)-1 \n"  \
  ;

  PyObject * DGTS_RebinTof2E_batch_numpyarray(PyObject *, PyObject *args)
  {
    PyObject *pytofbb, *pycntsmat, *pyerr2mat,
      *pyphibb, *pyebb, *pySmat, *pySerr2, *pyintsa,
      *pymaskarr, *pyphiarr, *pysaarr, *pydistarr,
      *pyradiusarr, *pypressurearr,
      *pytmpE, *pytmpI;
    npy_double ei, mod2sample;

    int ok = PyArg_ParseTuple
      (args, "OOOOOOOOddOOOOOOOO", 
       &pytofbb, &pycntsmat, &pyerr2mat,
       &pyphibb, &pyebb, &pySmat, &pySerr2, &pyintsa,
       &ei, &mod2sample, 
       &pymaskarr, &pyphiarr, &pysaarr, &pydistarr,
       &pyradiusarr, &pypressurearr,
       &pytmpE, &pytmpI);

    if (!ok) return 0;

    return DGTS_RebinTof2E_batch_impl::call_numpyarray
      <DblArrIt, NPY_DOUBLE,
      IntArrIt, NPY_INT,
      npy_double>
      (pytofbb, pycntsmat, pyerr2mat,
       pyphibb, pyebb, pySmat, pySerr2, pyintsa,
       pymaskarr, pyphiarr, pysaarr, pydistarr,
       pyradiusarr, pypressurearr,
       pytmpE, pytmpI,
       ei, mod2sample);

  }
    
} // reductionmod::



// version
// $Id: DGTS_RebinTof2E_batch_bdgs.h 512 2005-07-08 20:19:55Z tim $

// End of file
