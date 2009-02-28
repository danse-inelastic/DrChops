// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2009  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef H_ARCS_EVENTDATA_NORMALIZE_IhklE
#define H_ARCS_EVENTDATA_NORMALIZE_IhklE


#include "histogram/EvenlySpacedGridData_4D.h"
#include "AbstractMask.h"


namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_4D;

  typedef EvenlySpacedGridData_4D< double, double, double, double, double> SaHKLE;

  template <typename IhklE, typename Float, typename Index>
  void calcSolidAngleHKLE
  ( IhklE & sahkle, Float ei, Float *ub[3],
    Index npixels, 
    const Float * pixelpositions, const Float * pixelsolidangles,
    const AbstractMask & mask);

  template <typename Float>
  void calchkl( Float &h, Float &k, Float &l,
		const Float *position, Float ei, Float *ub[3], Float e );

}// ARCS_EventData


#include "normalize_ihkle.icc"

#endif 


// version
// $Id$

// End of file 
