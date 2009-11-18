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


#ifndef DANSE_REDUCTION_IPIX2IXY_H
#define DANSE_REDUCTION_IPIX2IXY_H


#include <cstring>

/// Reduce I(pixel) to I(x,y) 
/// with some magic this can be used to create things like
/// I(pixel, *) to I(x,y,*)

namespace DANSE { namespace Reduction{

    /// histogram I(pixel) to I(x,y)
    /// Is_begin, IsE2_begin: I(pixel)'s intensity/errorbar^2 arrays' beginning iterator
    /// xbb_begin/xbb_end: bin boundaries for x axis
    /// ybb_begin/ybb_end: bin boundaries for y axis
    /// outI_begin, outIE2_begin: I(x, y)'s intensity/errorbar^2 arrays' beginning iterator
    /// outsolidangle_begin, outsolidangleE2_begin: SolidAngle(x,y)'s intensity/errorbar^2 arrays' beginning iterator
    /// x_begin: x(pixel)'s beginning iter
    /// y_begin: y(pixel)'s beginning iter
    /// solidangle_begin/solidangleE2_begin: value/errorbar^2 of solidangle(pixel)
    /// mask_begin: mask(pixel)'s beginning iterator
    /// size: number of pixels
    template<
      typename Xvalue, typename Yvalue,
      typename XIterator, typename YIterator, typename IntensityIterator, typename SolidangleIterator,
      typename MaskIterator,
      typename XBinIterator, typename YBinIterator 
      >
    void Ipix2Ixy
    (
      XIterator x_begin, YIterator y_begin,
      IntensityIterator Is_begin, IntensityIterator IsE2_begin,
      SolidangleIterator solidangle_begin, SolidangleIterator solidangleE2_begin,
      MaskIterator mask_begin,
      size_t size,
      
      XBinIterator outxbb_begin, XBinIterator outxbb_end,
      YBinIterator outybb_begin, YBinIterator outybb_end,
      IntensityIterator outI_begin, IntensityIterator outIE2_begin,
      SolidangleIterator outsolidangle_begin, SolidangleIterator outsolidangleE2_begin
      );
  
}}//namespace DANSE::Reduction


#define DANSE_REDUCTION_IPIX2IXY_ICC
#include "Ipix2Ixy.icc"
#undef DANSE_REDUCTION_IPIX2IXY_ICC

#endif// DANSE_REDUCTION_IPIX2IXY_H

// version
// $Id$

// End of file 
