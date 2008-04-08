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


#ifndef DANSE_REDUCTION_PHITOSLICE_H
#define DANSE_REDUCTION_PHITOSLICE_H

#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif

#ifndef VALARRAY_INCLUDED
#define VALARRAY_INCLUDED
#include <valarray>   // for std::slice (sigh)
#endif


namespace DANSE{
  namespace Reduction {
    
    /// Functor to convert scattering angles to bin boundaries
    /// for S(phi, omega) histograms. 
    template <typename NumT>
    class PhiToSlice
    {
    public:
      /// angle must be greater than min angle in phi Bin Boundaries, or 
      ///     std::string("PhiToSlice<Numt>::phiToOffset() phi < phiMin") exception
      ///     will be thrown. Also, if the angle is greater than 
      ///     any angle in phiBinBoundaries, an exception 
      ///     std::string("PhiToSlice<Numt>::phiToOffset() phi > phiMax") 
      ///     will be thrown.
      std::slice operator()( NumT phi) const;
      size_t phiToOffset( NumT phi) const;
      
      /// ctor: arrayLength is the length of the histogram in
      ///     the other (energy) dimension. For DS2dv class,
      ///     this should be axis2Length() - 1.
      /// phiBinBoundaries is a ref to an array of the actual
      ///     angle bins used. Angles must be sorted from smallest
      ///     to largest.
      PhiToSlice( unsigned int arrayLength, 
		  std::vector<NumT> const & phiBinBoundaries);
    private:
      unsigned int m_arrLen;
      NumT m_dphi;    // delta phi, stored for convenience
      NumT m_phiMax;  // last value in phiBB, stored for convenience
      NumT m_phiMin;  // first value in phiBB
    };
    
  } // Reduction::
} // DANSE::

#endif // DANSE_REDUCTION_PHITOSLICE_H



// version
// $Id: PhiToSlice.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
