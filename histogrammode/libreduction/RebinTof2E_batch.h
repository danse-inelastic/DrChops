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


#ifndef DANSE_REDUCTION_REBINTOF2E_BATCH_H
#define DANSE_REDUCTION_REBINTOF2E_BATCH_H


#include "RebinTof2E.h"


namespace DANSE {

  namespace Reduction {
    
    namespace RebinTof2E_batch_impl {

      template <typename Iterator>
      void clear( Iterator it1, Iterator it2 ) {
	for (Iterator it = it1; it < it2; it++ ) {
	  *it = 0.;
	}
      }
      
    }// RebinTof2E_batch_impl::

    /// I(*,tof) --> I(E).
    /// Rebin I(tof) to I(E) for each pixel and add them all together
    /// to one I(E) spectrum.
    ///
    /// template parameters:
    ///   Real: The data type of all dereferenced iterators.
    ///   InputBinIterator: iterator for tof bins
    ///   InputIntensityIterator: iterator for I(tof) intensity array
    ///   OutputBinIterator: iterator for E bins
    ///   OutputIntensityIterator: iterator for I(E) intensity array
    ///   MaskIterator: iterator for mask(pixel) the mast array
    ///   DistanceInterator: iterator for distance(pixel) the distance array
    ///
    /// Arguments:
    ///   tofbb_begin: tof bin boundaries begin
    ///   tofbb_end:   tof bin boundaries end
    ///   inputI_begin: I(*,tof) array begin. tof index runs faster than the pixel index.
    ///   inputIerr2_begin: Ierror2(*,tof) array begin (error bar square). Indexing same as inutI_begin
    ///   ebb_begin:   energy bin boundaries begin
    ///   ebb_end:     energy bin boundaries end
    ///   outputI_begin: I(E) array begin
    ///   outputIerr2_begin: Ierror2(E) array begin (error bar square)
    ///   mask_begin:  mask(pixel) array begin
    ///   dist_begin:  distance(pixel) array begin (distance from moderator to pixel)
    ///   size_star:   number of pixels
    ///   tmpE:        temporary E array to store unevenly spaced energy bin boundaries
    ///                calculated from tof bin boundaries. Sizeof(tmpE)=sizeof(tofbb)
    ///   tmpI:        temporary I array to store rebinned I(E) array. sizeof(tmpI)=sizeof(ebb)
    template<
      typename Real, 
      typename InputBinIterator, typename InputIntensityIterator,
      typename OutputBinIterator, typename OutputIntensityIterator,
      typename DistanceIterator,
      typename MaskIterator
      >
    
    void Istartof2IE
    ( InputBinIterator tofbb_begin, InputBinIterator tofbb_end,
      InputIntensityIterator inputI_begin, InputIntensityIterator inputIerr2_begin,
      
      OutputBinIterator ebb_begin, OutputBinIterator ebb_end,
      OutputIntensityIterator outputI_begin, OutputIntensityIterator outputIerr2_begin,
      
      DistanceIterator dist_begin,
      MaskIterator mask_begin,
      
      size_t size_star,
      OutputBinIterator tmpE, OutputIntensityIterator tmpI )
    {
      using namespace RebinTof2E_batch_impl;

      typedef RebinTof2E< Real, InputBinIterator, InputIntensityIterator,
	OutputBinIterator, OutputIntensityIterator > RebinnerType;

      size_t nEbins = ebb_end - ebb_begin - 1,
	nTofbins = tofbb_end - tofbb_begin -1;
      
      // loop over all pixels
      for (size_t i = 0; i<size_star; i++) {

	if (*(mask_begin+i)) continue;
	
	RebinnerType rebinner( *(dist_begin + i) );

	//rebin I(tof) of a pixel to tmpI(E)
	clear(tmpI, tmpI+nEbins);
	rebinner(tofbb_begin, tofbb_end, inputI_begin + i*nTofbins,
		 tmpE, ebb_begin, ebb_end, tmpI);
	
	//add tmpI(E) to I(E)
	for (size_t j = 0; j<nEbins; j++) {
	  *(outputI_begin+j) += *(tmpI+j);
	}
	  
	//rebin Ierr2(tof) of a pixel to tmpI(E)
	clear(tmpI, tmpI+nEbins);
	rebinner(tofbb_begin, tofbb_end, inputIerr2_begin + i*nEbins,
		 tmpE, ebb_begin, ebb_end, tmpI);

	//add tmpI(E) to I(E)
	for (size_t j = 0; j<nEbins; j++)
	  *(outputIerr2_begin+j) += *(tmpI+j);

      }

    } // Itofstar2IE
    
  } // Reduction::
} // DANSE::


#endif // DANSE_REDUCTION_REBINTOF2E_BATCH_H


// version
// $Id$

// End of file 

