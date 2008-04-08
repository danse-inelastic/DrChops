// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "EBinCalcor_bdgs.h"
#include "EBinCalcor.h"

#include "reduction/utils.h"
#include "stdVector/utils.h"
#include "journal/debug.h"
#include <sstream>


namespace reductionmod
{
  int EBinCalcor__magicNumber__ = 490315662;
  
  namespace
  {
    const char journalname [] = "reductionmod";
    using journal::at;
    using journal::endl;
    
    template <typename NumT>
    PyObject *_callEBinCalcor_ctor( int dtype, 
				    NumT ei,
				    NumT modSampDist)
    {
      typedef DANSE::Reduction::EBinCalcor<NumT> CalcorT;
      
      CalcorT *newebc = 
	new CalcorT( ei, modSampDist);
      
      PyObject * retval = 
	DANSE::Reduction::utils::wrapObject<CalcorT >
	(newebc, dtype, reductionmod::EBinCalcor__magicNumber__);
      
      if ( retval == 0)
	{
	  journal::debug_t debug( journalname);
	  debug << at(__HERE__) << "wrapObject FAILED" << endl;
	  // exception context set in wrapObject
	}
      
      return retval;
    } // _callEBinCalcor_ctor( ...)
    
  } // anonymous::
  
  
  char EBinCalcor__name__[] = "EBinCalcor";
  char EBinCalcor__doc__[] = "EBinCalcor( datatype, incidentEnergy, modToSampleDist)\n"
	"Create a new energy bin calculator (to calculate old energy bins)\n"
	"inputs:\n"
	"    datatype      (datatype of vector; int)\n"
	"    incidentEnergy(in meV; float)\n"
	"    modSampDist   (distance from moderator to sample, in mm; float)\n"
	"output:\n"
	"    EBinCalcor instance of type <datatype> (PyCObject/TWrapper)\n"
	"Notes: 1) timeBinBounds should be neutron time of flight from\n"
	"moderator. If not, distance must match it.\n"
	"2) Recognized datatypes\n"
	"    float.....5\n"
	"    double....6\n"
	"Exceptions: ValueError";
  
  PyObject * EBinCalcor(PyObject *, PyObject *args)
  {
    int dtype = 0;
    double ei = 0.0, msd = 0.0;
    int ok = PyArg_ParseTuple( args, "idd", &dtype, &ei, &msd);
    if (!ok) return 0;
    
    std::string errstr("EBinCalcor() ");
    if (ei <= 0.0)
      {
	errstr += "kinetic energy usually positive";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    if (msd <= 0.0)
      {
	errstr += "moderator-sample distance must be > 0";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    
    switch (dtype)
      {
      case 5:   // float
	return _callEBinCalcor_ctor<float> ( dtype,
					     static_cast<float>(ei), 
					     static_cast<float>(msd));
      case 6:   // double
	return _callEBinCalcor_ctor<double>( dtype, ei, msd);
      default:
	errstr += "unrecognized datatype. Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
      }
    return 0;
  }
  
  
  namespace
  {
    template <typename FPT>
    bool _callEBinCalcor( PyObject *pyebc, 
			  FPT pixDist,
			  PyObject *pytbb, PyObject *pyebb, int dtype,
			  std::stringstream & errstr)
    {
      journal::debug_t debug( journalname);
      
      std::vector<FPT> * ptbb = 
	ARCSStdVector::unwrapVector<FPT> (pytbb, dtype);
      if( ptbb == 0)
	{
	  errstr << "unwrapVector tbb failed";
	  debug << at(__HERE__) <<  errstr.str() << endl;
	  return false;
	}
      
      std::vector<FPT> * pebb = 
	ARCSStdVector::unwrapVector<FPT> (pyebb, dtype);
      if( pebb == 0)
	{
	  errstr << "unwrapVector ebb failed";
	  debug << at(__HERE__) << errstr.str() << endl;
	  return false;
	}
      
      typedef DANSE::Reduction::EBinCalcor<FPT> CalcorT;

      CalcorT * pebc = 
	DANSE::Reduction::utils::unwrapObject<CalcorT >
	(pyebc, dtype);
      if( pebc == 0)
	{
	  errstr << "unwrapObject failed";
	  debug << at(__HERE__) << errstr.str() << endl;
	  return false;
	}
      
      try
	{
	  pebc->operator()( pixDist, *ptbb, *pebb);
	}
      catch( std::bad_alloc &ba)
	{
	  errstr << "Caught bad_alloc from EBinCalcor::"
		 << "operator(). Message: " << ba.what();
	  debug << at(__HERE__) << errstr.str() << endl;
	  return false;
	}
      
      return true;
    } // _callEBinCalcor( ... )
    
  } // anonymous::
  
  
  char EBinCalcorCall__name__[] = "EBinCalcor_Call";
  char EBinCalcorCall__doc__[] = 
        "EBinCalcor_Call( eBinCalcor, datatype, pixelDistance, tBinBounds, eBinBounds)\n"
        "Call an EBinCalcor object to compute energy bin bounds for a pixel\n"
        "and store the results in the vector binBounds.\n"
	"inputs:\n"
	"    eBinCalcor: EBinCalcor object\n"
	"    datatype: typecode (int)\n"
	"    pixelDistance: sample to pixel distance in mm (float)\n"
	"    tBinBounds: input vector (std::vector<datatype>)\n"
	"    eBinBounds: output vector (std::vector<datatype>)\n"
	"outputs: None\n"
	"Exceptions: ValueError."
	"Notes: (1) Recognized datatypes:\n"
	"          float....5\n"
	"          double...6\n"
	"(2) objects should be as wrapped by wrapObject<T> or wrapVector";
  
  PyObject * EBinCalcorCall(PyObject *, PyObject *args)
  {
    PyObject *pyebc = 0, *pyebb = 0, *pytbb = 0;
    int dtype = 0;
    double pixDist = 0.0;
    int ok = PyArg_ParseTuple( args, "OidOO", &pyebc, &dtype, &pixDist, 
			       &pytbb, &pyebb);
    if (!ok) return 0;
    
    std::stringstream errstr("EBinCalcorCall() ");
    journal::debug_t debug( journalname);
    bool okay = true;
    
    switch (dtype)
      {
      case 5:   // float
	okay = _callEBinCalcor<float> ( pyebc, pixDist, pytbb, pyebb, 
					dtype, errstr);
	break;
      case 6:   // double
	okay = _callEBinCalcor<double>( pyebc, pixDist, pytbb, pyebb, 
					dtype, errstr);
	break;
      default:
	errstr << "unrecognized datatype " << dtype 
	       << ". Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.str().c_str());
	return 0;
      }
    if( !okay)
      {
	debug << at(__HERE__) << "call did not complete as expected: "
	      << errstr.str() << endl;
	PyErr_SetString( PyExc_RuntimeError, errstr.str().c_str());
	return 0;
      }
    
    Py_INCREF(Py_None);
    return Py_None;
  }
  
  
} // reductionmod::


// version
// $Id: EBinCalcor_bdgs.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
