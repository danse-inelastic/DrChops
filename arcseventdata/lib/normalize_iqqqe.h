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


#ifndef H_ARCS_EVENTDATA_NORMALIZE_IQQQE
#define H_ARCS_EVENTDATA_NORMALIZE_IQQQE


#include "histogram/EvenlySpacedGridData_4D.h"
#include "AbstractMask.h"


namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_4D;

  typedef EvenlySpacedGridData_4D< double, double, double, double, double> SaQQQE;

  template <typename IQQQE, typename Float, typename Index>
  void calcSolidAngleQQQE
  ( IQQQE & saqqqe, Float ei, 
    Float pixelarea,
    Index npixels, const Float * pixelpositions, 
    const AbstractMask & mask);

  template <typename Float>
  void calcQQQ( Float &Qx, Float &Qy, Float &Qz,
		const Float *position, Float ei, Float e );

}// ARCS_EventData


#include "normalize_iqqqe.icc"

#endif 


// version
// $Id$

// End of file 
