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


#ifndef H_ARCS_EVENTDATA_IPIXTOF
#define H_ARCS_EVENTDATA_IPIXTOF


#include "histogram/EvenlySpacedGridData_2D.h"

namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_2D;

  typedef EvenlySpacedGridData_2D< unsigned int, unsigned int, unsigned int> Ipixtofc;
  typedef EvenlySpacedGridData_2D< unsigned int, double, unsigned int> Ipixtof;

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
