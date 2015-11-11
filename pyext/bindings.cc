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

#include "Itof2IE_batch_bdgs.h"
#include "IpixE2IphiE_bdgs.h"
#include "Zt2Zxy_bdgs.h"

// the method table

struct PyMethodDef pydrchops_methods[] = {

    {pydrchops_copyright__name__, pydrchops_copyright,
     METH_VARARGS, pydrchops_copyright__doc__},

    // Itof2IE_batch
    {reductionmod::Itof2IE_batch_numpyarray__name__, reductionmod::Itof2IE_batch_numpyarray,
     METH_VARARGS, reductionmod::Itof2IE_batch_numpyarray__doc__},

    // IpixE2IphiE
    {reductionmod::IpixE2IphiE_numpyarray__name__, reductionmod::IpixE2IphiE_numpyarray,
     METH_VARARGS, reductionmod::IpixE2IphiE_numpyarray__doc__},

    // Zt2Zxy
    {reductionmod::Zt2Zxy_numpyarray__name__, reductionmod::Zt2Zxy_numpyarray,
     METH_VARARGS, reductionmod::Zt2Zxy_numpyarray__doc__},


// Sentinel
    {0, 0}
};

// version
// $Id$

// End of file
