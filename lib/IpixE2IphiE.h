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


#ifndef DANSE_REDUCTION_IPIXE2IPHIE_H
#define DANSE_REDUCTION_IPIXE2IPHIE_H


#include <cstring>

/// Reduce I(pixel,E) to I(phi,E)

namespace DANSE { namespace Reduction{

    /// histogram I(pixel,E) to I(phi,E)
    /// ebb_begin/ebb_end: bin boundaries for E axis
    /// IEs_begin, IEsE2_begin: I(pixel, E)'s intensity/errorbar^2 arrays' beginning iterator
    /// outphibb_begin/outphibb_end: bin boundaries for phi axis
    /// outS_begin, outSE2_begin: I(phi, E)'s intensity/errorbar^2 arrays' beginning iterator
    /// outsolidangle_begin, outsolidangleE2_begin: SolidAngle(phi)'s intensity/errorbar^2 arrays' beginning iterator
    /// phi_begin: phi(pixel)
    /// solidangle_begin: solidangle(pixel)
    /// mask_begin: mask(pixel)'s beginning iterator
    /// size: number of pixels
    template<
      typename FLT, 
      typename InputBinIterator, typename InputDataIterator,
      typename OutputBinIterator, typename OutputDataIterator,
      typename MaskIterator
      >
    
    void IpixE2IphiE
    ( InputBinIterator ebb_begin, InputBinIterator ebb_end,
      InputDataIterator IEs_begin, InputDataIterator IEsE2_begin,
      
      OutputBinIterator outphibb_begin, OutputBinIterator outphibb_end,
      OutputDataIterator outS_begin, OutputDataIterator outSE2_begin,
      OutputDataIterator outsolidangle_begin, OutputDataIterator outsolidangleE2_begin,
      
      InputDataIterator phi_begin, 
      InputDataIterator solidangle_begin, InputDataIterator solidangleE2_begin,
      MaskIterator mask_begin,
      
      size_t size
      );
  
}}//namespace DANSE::Reduction


#define DANSE_REDUCTION_IPIXE2IPHIE_ICC
#include "IpixE2IPhiE.icc"
#undef DANSE_REDUCTION_IPIXE2IPHIE_ICC

#endif// DANSE_REDUCTION_IPIXE2IPHIE_H

// version
// $Id$

// End of file 
