// Timothy M. Kelley Copyright (c) 2005 All rights reserved

#include "QBinCalcor_bdgs.h"
#include "journal/debug.h"
#include "reduction/QBinCalcor.h"
#include "reduction/utils.h"
#include "stdVector/utils.h"

namespace
{
  using journal::at;
  using journal::endl;
  char journalname [] = "reductionmod";
} // anonymous::

namespace reductionmod
{
  int QBinCalcor__magicNumber__ = 58742569;

  namespace
  {
    template <typename NumT>
    PyObject *_callQBinCalcor_ctor( PyObject *pyphibb, int dtype,
				    NumT ei, bool inRadians)
    {
      journal::debug_t debug( journalname);

      std::vector<NumT> *pphibb = 
	ARCSStdVector::unwrapVector<NumT> (pyphibb, dtype);
      if( pphibb == 0)
	{
	  debug << at(__HERE__) << "unwrapVector phibb failed" << endl;
	  return 0; // exception context set in unwrapVector
	}
      
      using namespace DANSE::Reduction;

      QBinCalcor<NumT> *newqbc = 0;
      try
	{
	  newqbc = 
	    new QBinCalcor<NumT>( *pphibb, ei, inRadians);
	}
      catch( std::bad_alloc &ba)
	{
                
	  debug << at(__HERE__) << "allocation of QBinCalcor failed"
		<< endl;
	  PyErr_SetString( PyExc_RuntimeError, 
			   "allocation of QBinCalcor failed");
	  return 0;
	}

      PyObject *retval = 
	utils::wrapObject< QBinCalcor<NumT> >
	(newqbc, dtype, QBinCalcor__magicNumber__);

      if( retval == 0)
	{
	  debug << at(__HERE__) << "wrapObject for QBinCalcor failed"
		<< endl;
	}

      return retval;
    } // _callQBinCalcor
  } // anonymous::


  char QBinCalcor_ctor__name__[] = "QBinCalcor";
  char QBinCalcor_ctor__doc__[] = 
    "QBinCalcor( phiBinBounds, datatype, incidentEnergy, inRadians = 0)\n"
    "Create a new energy bin calculator (to calculate old energy bins)\n"
    "inputs:\n"
    "    phiBinBounds  (std::vector; PyCObject)\n"
    "    datatype      (datatype of vector; int)\n"
    "    incidentEnergy(in meV; float)\n"
    "    inRadians     (1: phi bin bnds in radians, 0: degrees (default); int)\n"
    "output:\n"
    "    QBinCalcor instance of type <datatype> (PyCObject)\n"
    "Notes: \n"
    "1) phiBinBounds should be angle measured from unscattered beam.\n"
    "2) Recognized datatypes\n"
    "    float.....5\n"
    "    double....6\n"
    "Exceptions: ValueError";

  PyObject * QBinCalcor_ctor(PyObject *, PyObject *args)
  {
    PyObject *pyphibb = 0;
    int dtype = 0;
    unsigned inRad = 0;
    double ei = 0.0;

    int ok = PyArg_ParseTuple( args, "Oid|I", &pyphibb, &dtype, &ei, 
			       &inRad);
    if (!ok) return 0;

    // check inputs: kinetic energy must be positive, inRadians must be
    // one or zero.
    std::string errstr("QBinCalcor() ");
    if (ei <= 0.0)
      {
	errstr += "kinetic energy usually positive";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    if( inRad > 1)
      {
	errstr += "inRadians must be one or zero";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    bool inRadians = false;
    if (inRad == 1) inRadians = true;

    switch (dtype)
      {
      case 5:   // float
	return _callQBinCalcor_ctor<float> ( pyphibb, dtype, 
					     static_cast<float>(ei), 
					     inRadians);
      case 6:   // double
	return _callQBinCalcor_ctor<double>( pyphibb, dtype, ei, inRadians);
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
    template <typename NumT>
    bool _callQBinCalcor( PyObject *pyqbc,
			  NumT ef,
			  PyObject *pyvec, int dtype)
    {
      journal::debug_t debug( journalname);

      std::vector<NumT> * pvec = 
	ARCSStdVector::unwrapVector<NumT> (pyvec, dtype);
      if(pvec == 0)
	{
	  debug << at(__HERE__) << "unwrapVector failed for pvec"
		<< endl;
	  return false;   // exception context set in unwrapVector
	}
      
      using namespace DANSE::Reduction;

      QBinCalcor<NumT> * pqbc = 
	utils::unwrapObject<QBinCalcor<NumT> >(pyqbc, dtype);
      if( pqbc == 0)
	{
	  debug << at(__HERE__) << "unwrapObject failed for QBinCalcor" 
		<< endl;
	  return false;   // exception context set in unwrapObject
	}
            
      pqbc->operator()( ef, *pvec);
      return true;
    }
  } // anonymous::
    

  char QBinCalcorCall__name__[] = "QBinCalcor_Call";
  char QBinCalcorCall__doc__[] = 
    "QBinCalcor_Call( eBinCalcor, datatype, e_final, binBounds)\n"
    "Call an QBinCalcor object to compute energy bin bounds for a pixel\n"
    "and store the results in the vector binBounds.\n"
    "inputs:\n"
    "    eBinCalcor (QBinCalcor object; PyCObject)\n"
    "    datatype ..(int)\n"
    "    e_final ...(final neutron energy, in meV, float)\n"
    "    binBounds .(std::vector<datatype>; PyCObject)\n"
    "outputs: None\n"
    "Notes: Recognized datatypes:\n"
    "          float....5\n"
    "          double...6\n"
    "Exceptions: ValueError";

  PyObject * QBinCalcorCall(PyObject *, PyObject *args)
  {
    PyObject *pyqbc = 0, *pyvec = 0;
    double ef = 0.0;
    int dtype = 0;
    int ok = PyArg_ParseTuple( args, "OidO", &pyqbc, &dtype, &ef, &pyvec);
    if (!ok) return 0;

    std::string errstr("QBinCalcorCall() ");

    switch (dtype)
      {
      case 5:   // float
	_callQBinCalcor<float> ( pyqbc, static_cast<float>(ef), pyvec, dtype);
	break;
      case 6:   // double
	_callQBinCalcor<double>( pyqbc, ef, pyvec, dtype);
	break;
      default:
	errstr += "unrecognized datatype. Recognized datatypes:\n"
	  "          float....5\n"
	  "          double...6\n";
	PyErr_SetString( PyExc_ValueError, errstr.c_str());
	return 0;
      }
    Py_INCREF(Py_None);
    return Py_None;
  }

} // reductionmod::



// version
// $Id: QBinCalcor_bdgs.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
