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


#ifndef DANSE_REDUCTION_ZT2ZXY_H
#define DANSE_REDUCTION_ZT2ZXY_H


#include <cstring>

/// Reduce Z(t) to Z(x,y)
/// with some magic this can be used to create things like
/// I(pixel, *) to I(phi,psi,*)

namespace DANSE { namespace Reduction{

    /// histogram Z(t) to Z(x,y)
    /// z_begin: Z(t)'s beginning iterator
    /// outxbb_begin/outxbb_end: bin boundaries for output x axis
    /// outybb_begin/outybb_end: bin boundaries for output y axis
    /// outz_begin: Z(x, y)'s beginning iterator
    /// x_begin: x(t)'s beginning iter
    /// y_begin: y(t)'s beginning iter
    /// size: number of t values
    template<
      typename Xvalue, typename Yvalue, typename Zvalue,
      typename InputXIterator, typename InputYIterator, typename InputZIterator,
      typename MaskIterator,
      typename OutputXBinIterator, typename OutputYBinIterator, typename OutputZIterator
      >
    
    void Zt2Zxy
    ( 
      InputXIterator x_begin, InputYIterator y_begin,
      InputZIterator z_begin,
      MaskIterator mask_begin,
      size_t size,
      OutputXBinIterator outxbb_begin, OutputXBinIterator outxbb_end,
      OutputYBinIterator outybb_begin, OutputYBinIterator outybb_end,
      
      OutputZIterator outz_begin
      );
  
}}//namespace DANSE::Reduction


#define DANSE_REDUCTION_ZT2ZXY_ICC
#include "Zt2Zxy.icc"
#undef DANSE_REDUCTION_ZT2ZXY_ICC

#endif// DANSE_REDUCTION_ZT2ZXY_H

// version
// $Id$

// End of file 
