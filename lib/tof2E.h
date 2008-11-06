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

#ifndef DANSE_REDUCTION_TOF2E_H
#define DANSE_REDUCTION_TOF2E_H

#include "physics.h"

namespace DANSE {
  namespace Reduction {
    
    // convert time of flight to energy
    // tof: musec
    // distance: mm
    // energy: meV
    template <typename FLT>
    FLT tof2E( FLT tof, FLT distance)
    {
      using namespace DANSE::Physics::Units::Conversion;
      return v2E(distance/tof * 1000.);
    }
    
    // convert an array of time of flight to energy
    // tofs: musec
    // distance: mm
    // energy: meV
    // tof_begin: const iterator. begin of tof array
    // tof_end: const iterator. end of tof array
    // energy_begin: iterator. The energy array must have the same size as the tof array
    template < typename ConstIterator, typename Iterator, typename FLT >
    void tof2E( ConstIterator tof_begin, ConstIterator tof_end, FLT distance, 
		Iterator energy_begin )
    {
      ConstIterator tofit;
      for (tofit = tof_begin; tofit < tof_end; tofit++, energy_begin++) {
	*energy_begin = tof2E( *tofit, distance );
      }
    }
    
  } // Reduction::
}// DANSE::

#endif// DANSE_REDUCTION_TOF2E_H

// version
// $Id$

// End of file 
