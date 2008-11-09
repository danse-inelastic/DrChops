// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                      (C) 2007-2008  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef DANSE_REDUCTION_ITOF2IE_BATCH_H
#define DANSE_REDUCTION_ITOF2IE_BATCH_H


#include <cstring>

/// Reduce I(*,tof) to I(*,E)

namespace DANSE { namespace Reduction{

  template<
    typename FLT, 
    typename InputBinIterator, typename InputDataIterator,
    typename OutputBinIterator, typename OutputDataIterator
    >
  
  void Itof2IE_batch
  ( InputBinIterator tofbb_begin, InputBinIterator tofbb_end,
    InputDataIterator Itofs_begin, InputDataIterator ItofsE2_begin,

    OutputBinIterator ebb_begin, OutputBinIterator ebb_end,
    OutputDataIterator IEs_begin, OutputDataIterator IEsE2_begin,

    FLT ei, FLT mod2sample, 

    InputDataIterator dist_begin,
    size_t size,
    OutputBinIterator tmpE);
  
}}//namespace DANSE::Reduction


#define DANSE_REDUCTION_ITOF2IE_BATCH_ICC
#include "Itof2IE_batch.icc"
#undef DANSE_REDUCTION_ITOF2IE_BATCH_ICC

#endif// DANSE_REDUCTION_ITOF2IE_BATCH_H

// version
// $Id$

// End of file 
