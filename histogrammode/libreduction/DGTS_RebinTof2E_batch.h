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


#ifndef DANSE_REDUCTION_DGTS_REBINTOF2E_BATCH_H
#define DANSE_REDUCTION_DGTS_REBINTOF2E_BATCH_H


#include <cstring>

/// Reduce I(*,tof) to I(phi,E)

namespace DANSE { namespace Reduction{

  template<
    typename FLT, 
    typename InputBinIterator, typename InputDataIterator,
    typename OutputBinIterator, typename OutputDataIterator,
    typename MaskIterator,
    typename EfficiencyCorrector> 
  
  void DGTS_RebinTof2E_batch
  ( InputBinIterator tofbb_begin, InputBinIterator tofbb_end,
    InputDataIterator cnts_begin, InputDataIterator error2_begin,

    OutputBinIterator phibb_begin, OutputBinIterator phibb_end,
    OutputBinIterator ebb_begin, OutputBinIterator ebb_end,
    OutputDataIterator S_begin, OutputDataIterator Serr2_begin,
    OutputDataIterator outsolidangle_begin,

    FLT ei, FLT mod2sample, 

    MaskIterator mask_begin,
    InputDataIterator phi_begin, InputDataIterator solidangle_begin,
    InputDataIterator dist_begin,
    InputDataIterator radius_begin, InputDataIterator pressure_begin,
    size_t size,
    OutputBinIterator tmpE, OutputDataIterator tmpI );
  
}}//namespace DANSE::Reduction


#define DANSE_REDUCTION_DGTS_REBINTOF2E_BATCH_ICC
#include "DGTS_RebinTof2E_batch.icc"
#undef DANSE_REDUCTION_DGTS_REBINTOF2E_BATCH_ICC

#endif// DANSE_REDUCTION_DGTS_REBINTOF2E_BATCH_H

// version
// $Id$

// End of file 
