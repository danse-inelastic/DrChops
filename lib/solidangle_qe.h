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


#ifndef DRCHOPS_SOLIDANGLE_QE_H
#define DRCHOPS_SOLIDANGLE_QE_H


#include "histogram/EvenlySpacedGridData_2D.h"

#include "_macros.h"


DRCHOPS_NAMESPACE_START


USING_HISTOGRAM_NAMESPACE;

// type that can be used as template parameter IQE for
// method calcSolidAngleQE
typedef EvenlySpacedGridData_2D< double, double, double> SaQE;


// calculate solid angle (Q,E) histogram
// - saqe: result histogram
// - ei: incident eenrgy (meV)
// - npixels: # of pixels
// - pixelpositions: Float array of size npixels*3.  
//       pixelpositions[3*n:3*n+3] is the position vector of pixel n
//       unit: meter
// - pixelsolidangles: solid angles of pixels. size: npixels. unit: sr
// - mask: boolean array of size npixels. could be NULL
template <typename IQE, typename Float, typename Index>
void calcSolidAngleQE
( IQE & saqe, Float ei, 
  Index npixels, 
  const Float * pixelpositions, const Float * pixelsolidangles,
  const bool * mask=NULL);

template <typename Float>
Float calcQ( const Float *position, Float ei, Float e );


DRCHOPS_NAMESPACE_END

#include "solidangle_qe.icc"

#endif 


// version
// $Id$

// End of file 
