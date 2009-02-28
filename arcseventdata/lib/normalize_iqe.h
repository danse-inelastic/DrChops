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


#ifndef H_ARCS_EVENTDATA_NORMALIZE_IQE
#define H_ARCS_EVENTDATA_NORMALIZE_IQE


#include "histogram/EvenlySpacedGridData_2D.h"
#include "AbstractMask.h"


namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_2D;

  typedef EvenlySpacedGridData_2D< double, double, double> SaQE;

  template <typename IQE, typename Float, typename Index>
  void calcSolidAngleQE
  ( IQE & saqe, Float ei, 
    Index npixels, 
    const Float * pixelpositions, const Float * pixelsolidangles,
    const AbstractMask & mask);

  template <typename Float>
  Float calcQ( const Float *position, Float ei, Float e );

}// ARCS_EventData


#include "normalize_iqe.icc"

#endif 


// version
// $Id$

// End of file 
