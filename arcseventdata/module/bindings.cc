// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               Michael A.G. Aivazis
//                        California Institute of Technology
//                        (C) 1998-2005  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "bindings.h"

#include "misc.h"          // miscellaneous methods

#include "wrap_events2EvenlySpacedIx.h"
#include "wrap_events2EvenlySpacedIxy.h"
#include "wrap_events2EvenlySpacedIxxxx.h"
#include "wrap_readevents.h"
#include "wrap_readpixelpositions.h"
#include "wrap_mslice_formating.h"
#include "wrap_normalize_iqe.h"
#include "wrap_normalize_iqqqe.h"


// the method table

struct PyMethodDef pyarcseventdata_methods[] = {

    // dummy entry for testing
    {pyarcseventdata_hello__name__, pyarcseventdata_hello,
     METH_VARARGS, pyarcseventdata_hello__doc__},

    {pyarcseventdata_copyright__name__, pyarcseventdata_copyright,
     METH_VARARGS, pyarcseventdata_copyright__doc__},

    // events2Ipix
    {wrap_arcseventdata::events2Ipix_numpyarray__name__, 
     wrap_arcseventdata::events2Ipix_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2Ipix_numpyarray__doc__},
    
    // events2Itof
    {wrap_arcseventdata::events2Itof_numpyarray__name__, 
     wrap_arcseventdata::events2Itof_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2Itof_numpyarray__doc__},
    
    // events2Idspacing
    {wrap_arcseventdata::events2Idspacing_numpyarray__name__, 
     wrap_arcseventdata::events2Idspacing_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2Idspacing_numpyarray__doc__},

    // events2IpixE
    {wrap_arcseventdata::events2IpixE_numpyarray__name__, 
     wrap_arcseventdata::events2IpixE_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2IpixE_numpyarray__doc__},
        
    // events2IQE
    {wrap_arcseventdata::events2IQE_numpyarray__name__, 
     wrap_arcseventdata::events2IQE_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2IQE_numpyarray__doc__},
    
    // events2Ipixtof
    {wrap_arcseventdata::events2Ipixtof_numpyarray__name__, 
     wrap_arcseventdata::events2Ipixtof_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2Ipixtof_numpyarray__doc__},
    
    // events2Ipixd
    {wrap_arcseventdata::events2Ipixd_numpyarray__name__, 
     wrap_arcseventdata::events2Ipixd_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2Ipixd_numpyarray__doc__},
    
    // events2IQQQE
    {wrap_arcseventdata::events2IQQQE_numpyarray__name__, 
     wrap_arcseventdata::events2IQQQE_numpyarray,
     METH_VARARGS, wrap_arcseventdata::events2IQQQE_numpyarray__doc__},
    
    // readevents
    {wrap_arcseventdata::readevents__name__, 
     wrap_arcseventdata::readevents,
     METH_VARARGS, wrap_arcseventdata::readevents__doc__},
    
    // readpixelpositions
    {wrap_arcseventdata::readpixelpositions__name__, 
     wrap_arcseventdata::readpixelpositions,
     METH_VARARGS, wrap_arcseventdata::readpixelpositions__doc__},
    
    // SGrid_str
    {wrap_arcseventdata::SGrid_str_numpyarray__name__, 
     wrap_arcseventdata::SGrid_str_numpyarray,
     METH_VARARGS, wrap_arcseventdata::SGrid_str_numpyarray__doc__},
    
    // calcSolidAngleQE
    {wrap_arcseventdata::calcSolidAngleQE_numpyarray__name__, 
     wrap_arcseventdata::calcSolidAngleQE_numpyarray,
     METH_VARARGS, wrap_arcseventdata::calcSolidAngleQE_numpyarray__doc__},

    // calcSolidAngleQQQE
    {wrap_arcseventdata::calcSolidAngleQQQE_numpyarray__name__, 
     wrap_arcseventdata::calcSolidAngleQQQE_numpyarray,
     METH_VARARGS, wrap_arcseventdata::calcSolidAngleQQQE_numpyarray__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
