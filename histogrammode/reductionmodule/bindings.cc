// -*- C++ -*-
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 
//                               T. M. Kelley
//                        California Institute of Technology
//                        (C) 1998-2004  All Rights Reserved
// 
//  <LicenseText>
// 
//  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// 

#include <portinfo>
#include <Python.h>

#include "bindings.h"

#include "misc.h"          // miscellaneous methods
#include "absorptionmod.h"
#include "EBinCalcor_bdgs.h"
#include "ERebinAllInOne_bdgs.h"
#include "He3DetEffic_bdgs.h"
#include "QBinCalcor_bdgs.h"
#include "RDriver_bdgs.h"
#include "VecAccum_bdgs.h"
#include "RebinTof2E_bdgs.h"
#include "RebinTof2E_batch_bdgs.h"
#include "DGTS_RebinTof2E_batch_bdgs.h"

// the method table

struct PyMethodDef pyreduction_methods[] = {

    // dummy entry for testing
    {pyreduction_copyright__name__, pyreduction_copyright,
     METH_VARARGS, pyreduction_copyright__doc__},

    // He3 detector efficiency bindings
    {reductionmod::He3DetEffic__name__, reductionmod::He3DetEffic, 
     METH_VARARGS, reductionmod::He3DetEffic__doc__},
    {reductionmod::He3DetEfficExecSingle__name__, 
     reductionmod::He3DetEfficExecSingle, 
     METH_VARARGS, reductionmod::He3DetEfficExecSingle__doc__},
    {reductionmod::He3DetEfficExecVector__name__, 
     reductionmod::He3DetEfficExecVector, 
     METH_VARARGS, reductionmod::He3DetEfficExecVector__doc__},
    {reductionmod::He3DetEffic_classID__name__, 
     reductionmod::He3DetEffic_classID, 
     METH_VARARGS, reductionmod::He3DetEffic_classID__doc__},

    // VanPlateTx
    {reductionmod::vanPlateXmission_ctor__name__, 
     reductionmod::vanPlateXmission_ctor,
     METH_VARARGS, reductionmod::vanPlateXmission_ctor__doc__},
    {reductionmod::vanPlateXmission_call__name__, 
     reductionmod::vanPlateXmission_call,
     METH_VARARGS, reductionmod::vanPlateXmission_call__doc__},

    // EBinCalcor
    {reductionmod::EBinCalcor__name__, reductionmod::EBinCalcor,
     METH_VARARGS, reductionmod::EBinCalcor__doc__},
    {reductionmod::EBinCalcorCall__name__, reductionmod::EBinCalcorCall,
     METH_VARARGS, reductionmod::EBinCalcorCall__doc__},

    // ERebinAllInOne
    {reductionmod::ERebinAllInOne_ctor__name__, 
     reductionmod::ERebinAllInOne_ctor,
     METH_VARARGS, reductionmod::ERebinAllInOne_ctor__doc__},
    {reductionmod::ERebinAllInOne_call__name__, 
     reductionmod::ERebinAllInOne_call,
     METH_VARARGS, reductionmod::ERebinAllInOne_call__doc__},

    // QBinCalcor
    {reductionmod::QBinCalcor_ctor__name__,
     reductionmod::QBinCalcor_ctor, 
     METH_VARARGS, reductionmod::QBinCalcor_ctor__doc__},
    {reductionmod::QBinCalcorCall__name__, reductionmod::QBinCalcorCall, 
     METH_VARARGS, reductionmod::QBinCalcorCall__doc__},

    // RDriver
    {reductionmod::RDriver__name__, reductionmod::RDriver,
     METH_VARARGS, reductionmod::RDriver__doc__},
    {reductionmod::RDriver_call__name__, reductionmod::RDriver_call,
     METH_VARARGS, reductionmod::RDriver_call__doc__},
    {reductionmod::RDriver_norms__name__, reductionmod::RDriver_norms,
     METH_VARARGS, reductionmod::RDriver_norms__doc__},

    // VecAccum
    {reductionmod::VecAccum__name__, reductionmod::VecAccum, 
     METH_VARARGS, reductionmod::VecAccum__doc__},


    // RebinTof2E
    {reductionmod::RebinTof2E__name__, reductionmod::RebinTof2E,
     METH_VARARGS, reductionmod::RebinTof2E__doc__},
    {reductionmod::RebinTof2ECall_numpyarray__name__, reductionmod::RebinTof2ECall_numpyarray,
     METH_VARARGS, reductionmod::RebinTof2ECall_numpyarray__doc__},
    
    // RebinTof2E_batch
    {reductionmod::Istartof2IE_numpyarray__name__, reductionmod::Istartof2IE_numpyarray,
     METH_VARARGS, reductionmod::Istartof2IE_numpyarray__doc__},

    // DGTS_RebinTof2E_batch
    {reductionmod::DGTS_RebinTof2E_batch_numpyarray__name__, reductionmod::DGTS_RebinTof2E_batch_numpyarray,
     METH_VARARGS, reductionmod::DGTS_RebinTof2E_batch_numpyarray__doc__},
    
// Sentinel
    {0, 0}
};

// version
// $Id: bindings.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
