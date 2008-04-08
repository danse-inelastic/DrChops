// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2005-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef DANSE_REDUCTION_EREBINALLINONE_H
#define DANSE_REDUCTION_EREBINALLINONE_H

#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif

namespace DANSE {
  namespace Reduction {
    
    /// Computes the overlap matrix and multiplies it in one step for each 
    /// pixel.
    /// Template parameter:
    ///     FPT: floating point type
    ///     VT:  vector type (default FPT*)
    ///     ItT: Iterator type (default FPT*)
    ///     SzT: size_t for VT
    /// No iterator version is presently implemented.
    /// The only thing potentially energy dependent about it is the name.
    template <typename FPT, typename VT = std::vector<FPT>, 
	      typename SzT = size_t, typename ItT = FPT*>
    class ERebinAllInOne
    {
    public:
      /// execute
      /// Parameters:
      ///     oldBounds: old bin boundaries
      ///     newBounds: new bin boundaries
      ///     inData: array of input data
      ///     inErrs: array of input errors, ALREADY SQUARED
      ///     outData: output data will be placed here.
      ///     outErrs: output errs SQUARED will be placed here.
      void operator()( VT const & oldBounds, VT const & newBounds, 
		       VT const & inData, VT const & inerrs,
		       VT & outData, VT & outErrs);
      
      /// ctor: 
      /// Parameters:
      ///     numOldBins: How many bins in old array
      ///     numNewBins: How many bins in new array
      ///     dtOverde: width of old bin divided by width of new bin
      ///     kPrimeOverK: whether to apply k'/k correction
      ///     ei: if previous was true, incident energy to use
      ERebinAllInOne( SzT numOldBins, SzT numNewBins,
		      FPT dtOverde,
		      bool kPrimeOverK = false, FPT ei = 25.3)
	: m_nold(numOldBins + 1), m_nnew( numNewBins + 1), 
	  m_dtOverde( dtOverde),
	  m_kpok( kPrimeOverK ), m_ei( ei){}
    private:
      SzT m_nold, m_nnew; 
      FPT m_dtOverde;
      bool m_kpok;
      FPT m_ei;
      
      FPT greaterof( FPT a, FPT b){ return (a > b) ? a : b;}
      FPT lesserof( FPT a, FPT b) { return (a < b) ? a : b;}
    };

  } // Reduction::
  
} // DANSE::

// template function definitions--no instantiations!
#define DANSE_REDUCTION_EREBINALLINONE_ICC
#include "ERebinAllInOne.icc"
#undef DANSE_REDUCTION_EREBINALLINONE_ICC

#endif


// version
// $Id: ERebinAllInOne.h 1432 2007-11-04 02:10:13Z linjiao $

// End of file
