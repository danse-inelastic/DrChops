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


#ifndef H_ARCS_EVENTDATA_ITOF
#define H_ARCS_EVENTDATA_ITOF


#include "histogram/EvenlySpacedGridData_1D.h"

namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_1D;

  typedef EvenlySpacedGridData_1D< unsigned int, unsigned int> Itofchannel;
  typedef EvenlySpacedGridData_1D< double, unsigned int> Itof;

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
