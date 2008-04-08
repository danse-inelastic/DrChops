// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2003-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#ifndef DANSE_REDUCTION_RDRIVER_H
#define DANSE_REDUCTION_RDRIVER_H

#ifndef VECACCUM_INCLUDED
#define VECACCUM_INCLUDED
#include "VecAccum.h"
#endif

#ifndef PHITOSLICE_INCLUDED
#define PHITOSLICE_INCLUDED
#include "PhiToSlice.h"
#endif


namespace DANSE {
  namespace Reduction {
    
    /// add I(E) of a pixel to S(phi,E) given phi 
    template <typename NumT>
    class RDriver
    {
    public:
      typedef std::vector<NumT> VecNum;
      void ring( VecNum const & source,
		 NumT scatteringAngle);
      const VecNum & norms() const { return m_norms; }
      RDriver( VecNum & speHist,
	       size_t otherArrayLength,
	       VecNum & phiBB);
      ~RDriver();
    private:
      VecAccum<NumT> m_accum;
      PhiToSlice<NumT> m_speSlicer;
      VecNum m_norms;
    };

  } // Reduction::
} // DANSE::

#endif // DANSE_REDUCTION_RDRIVER_H


// version
// $Id: RDriver.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
