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


#include "DGTS_RebinTof2E_batch.h"
#include "He3EfficiencyCorrection.h"

namespace DANSE {
  namespace Reduction {
    
    //explicit instantiations
    template void DGTS_RebinTof2E_batch<
      double,
      double *, double *, double *, double *, bool *, 
      He3EfficiencyCorrection<double, std::vector<double>::iterator, double * >
      >
    ( double * tofbb_begin, double * tofbb_end,
      double * cnts_begin, double * error2_begin,
      
      double * phibb_begin, double * phibb_end,
      double * ebb_begin, double * ebb_end,
      double * S_begin, double * Serr2_begin,
      double * outsolidangle_begin,
      
      double ei, double mod2sample, 
      
      bool * mask_begin,
      double * phi_begin, double * solidangle_begin,
      double * dist_begin,
      double * radius_begin, double * pressure_begin,
      size_t size,
      double * tmpE, double * tmpI );
    
  } // Reduction::
} // DANSE::

// version
// $Id: He3DetEffic.cc 1443 2007-11-15 07:17:37Z linjiao $

// End of file


