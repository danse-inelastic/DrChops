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

#ifndef DANSE_REDUCTION_EBINCALCOR_H
#define DANSE_REDUCTION_EBINCALCOR_H

// #ifndef PHAROSPIXEL_INCLUDED
// #define PHAROSPIXEL_INCLUDED
// #include <PharosPixel.h>
// #endif

// #ifndef VALARRAY_INCLUDED
// #define VALARRAY_INCLUDED
// #include <valarray>
// #endif

#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif


namespace DANSE { namespace Reduction {

    /// EBinCalcor: compute energy bins, given time bin bounds, incident 
    /// energy, and distance from moderator to sample.
    /// Please note that the energy calculated is the energy difference:
    ///  Ei - Ef.
    /// template type FPT: floating point type
    template <typename FPT>
    class EBinCalcor
    {
    public:
      /// incidentEnergy in meV
      /// moderator to sample distance in mm)
      EBinCalcor( FPT incidentEnergy, 
		  FPT modToSampDist);
      
      /// compute energy bin boundaries
      /// pixelDistance: distance from sample to pixel in mm
      /// tBinBounds: vector with time bin boundaries, in microsec from T0
      /// eBinBounds: vector for output
      /// eBinBounds will be resized if not same size as tBinBounds; 
      /// bad_alloc will be thrown if this allocation fails.
      void operator()( FPT pixelDistance, 
		       std::vector<FPT> const & tBinBounds,
		       std::vector<FPT> &eBinBounds);
      
    private:
      FPT m_ei, m_lToSamp, m_vi;  
    };
    
  } // Reduction
} // DANSE
  
// include template definitions--no instantiations!!!
#define DANSE_REDUCTION_EBINCALCOR_ICC
#include "EBinCalcor.icc"
#undef DANSE_REDUCTION_EBINCALCOR_ICC


#endif // DANSE_REDUCTION_EBINCALCOR_H



// version
// $Id: EBinCalcor.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
