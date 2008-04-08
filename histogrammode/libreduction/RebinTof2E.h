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


#ifndef DANSE_REDUCTION_REBINTOF2E_H
#define DANSE_REDUCTION_REBINTOF2E_H


#include "Functor.h"
#include "tof2E.h"
#include "Universal1DRebinner.h"


namespace DANSE{
  namespace Reduction{
    
    /// functor: tof --> E.
    /// This is a functor to convert time of flight to neutron energy
    template <typename FLT>
    class Tof2EFunctor: public Reduction::Functor<FLT, FLT> {
    public:
      Tof2EFunctor( FLT distance ) 
	: m_distance(distance)
      {}
      
      virtual FLT operator() ( const FLT & tof ) {
	return tof2E( tof, m_distance );
      }
      
    private:
      FLT m_distance;
    };
    
    
    /// this rebinner rebin tof to energy 
    /// Please note that this rebinner is different from 
    /// other similar rebinners. Some rebinners rebin tof to Ei-Ef,
    /// some may rebin tof to Ef-Ei, etc etc
    /// this rebinner simply rebin tof of neutron to energy of neutron.
    /// template parameters:
    ///   - FLT: data type of all dereferenced iterators
    ///   - InputBinIterator: tof bin iterator type
    ///   - InputIntensityIterator: I(tof) intensity array iterator
    ///   - OutputBinIterator: E bin interator
    ///   - OutputIntensityIterator: I(E) intensity array iterator
    template <typename FLT, 
	      typename InputBinIterator,
	      typename InputIntensityIterator = InputBinIterator,
	      typename OutputBinIterator = InputBinIterator,
	      typename OutputIntensityIterator = OutputBinIterator
	      >
    class RebinTof2E {
      
    public:
      
      RebinTof2E( FLT distance ) : m_functor( distance ) {}
      
      typedef Reduction::Universal1DRebinner
      < FLT,
	InputBinIterator, 
	FLT,
	InputIntensityIterator,
	FLT,
	OutputBinIterator,
	FLT,
	OutputIntensityIterator
	> URebinner ;
      
      void operator() 
      ( InputBinIterator tofBegin, InputBinIterator tofEnd,
	InputIntensityIterator ItofBegin,
	OutputBinIterator tmpEBegin,
	OutputBinIterator EBegin, OutputBinIterator EEnd,
	OutputIntensityIterator IEBegin )
      {
	m_rebinner( tofBegin, tofEnd, ItofBegin,
		    tmpEBegin, EBegin, EEnd, IEBegin,
		    m_functor);
      }
      
      
    private:
      URebinner m_rebinner;
      Tof2EFunctor<FLT> m_functor;
    };
    
  } //namespace Reduction
} //namespace DANSE

#endif// DANSE_REDUCTION_REBINTOF2E_H

// version
// $Id$

// End of file 
