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


#ifndef REDUCTION_REBINTOF2E_H
#define REDUCTION_REBINTOF2E_H

#include "exception.h"
#include "Functor.h"
#include "sort.h"
#include "tof2E.h"
#include "Universal1DRebinner.h"


namespace DANSE{
  namespace Reduction{
    
    template <typename FLT>
    class DGTS_Tof2EFunctor: public Functor<FLT, FLT> {
    public:
      DGTS_Tof2EFunctor( FLT ei, FLT mod2sample, FLT distance )
	: m_distance(distance), m_ei( ei ), m_mod2sample(mod2sample)
      {
	using DANSE::Physics::Units::Conversion::E2v;
	FLT vi = E2v( ei );
	m_tof0 = m_mod2sample/vi*1000.;
      }
      
      void set_distance( FLT distance ) { m_distance = distance; }
      
      virtual FLT operator() ( const FLT & tof ) {
	FLT tof1 = tof - m_tof0;
	if (tof1<0) { throw Exception("negative energy resulted from unphysical tof axis. Please restrict the tof axis to physical region"); }
	return m_ei - tof2E( tof1, m_distance );
      }
      
    private:
      FLT m_distance, m_ei, m_mod2sample, m_tof0;
    };
    
    
    /// calculate time of flight from moderator to sample given neutron incident energy
    /// arguments:
    ///   ei: incident energy. unit: meV
    ///   mod2sample: moderator to sample distance. unit: meter
    ///
    template <typename FLT>
    FLT tof_mod2sample( const FLT & ei, const FLT & mod2sample)
    {
      using DANSE::Physics::Units::Conversion::E2v;
      return mod2sample / E2v(ei) * 1000.;  
    }
    
    
    /// this rebinner rebin tof to Ei-Ef
    /// It works for direct-geometry time-of-flight spectrometer.
    /// Please note that this rebinner is different from 
    /// other similar rebinners. Some rebinners rebin tof to neutron energy,
    /// some may rebin tof to Ef-Ei, etc etc
    /// 
    template <
      typename FLT ,
      typename InputBinIterator ,
      typename InputIntensityIterator,
      typename OutputBinIterator ,
      typename OutputIntensityIterator
      >  
    class DGTS_RebinTof2E {
      
    public:
      
      DGTS_RebinTof2E( FLT ei, FLT mod2sample ) 
	: m_functor( ei, mod2sample, 0.0 ), m_tof0( tof_mod2sample(ei, mod2sample) )
      {}
      
      typedef Universal1DRebinner
      < FLT,
	InputBinIterator,
	FLT,
	InputIntensityIterator, 
	FLT,
	OutputBinIterator,
	FLT,
	OutputIntensityIterator
	> URebinner ;
      
      void set_distance( FLT distance ) { m_functor.set_distance( distance ); }
      
      void operator() 
      ( InputBinIterator tofBegin, InputBinIterator tofEnd,
	InputIntensityIterator ItofBegin,
	OutputBinIterator tmpEBegin,
	OutputBinIterator EBegin, OutputBinIterator EEnd,
	OutputIntensityIterator IEBegin )
      {
	//       std::cout << "tof0=" << m_tof0 << ","
	// 		<< "tofBegin=" << *tofBegin << ","
	// 		<< "tofEnd=" << *(tofEnd-1) << ","
	// 		<< std::endl;
	
	if (*tofBegin <= m_tof0) {
	  if (m_tof0>=*(tofEnd-1)) throw( Exception( "tof axis totally nonsense. all tof values are unphysical" ) );
	  
	  size_t i = findCellIndex( m_tof0, tofBegin, tofEnd ) + 1;
	  
	  m_rebinner( tofBegin+i, tofEnd, ItofBegin+i,
		      tmpEBegin, EBegin, EEnd, IEBegin,
		      m_functor);
	  
	} else {
	  
	  m_rebinner( tofBegin, tofEnd, ItofBegin,
		      tmpEBegin, EBegin, EEnd, IEBegin,
		      m_functor);
	  
	}
	
      }
      
    private:
      URebinner m_rebinner;
      DGTS_Tof2EFunctor<FLT> m_functor;
      FLT m_tof0;
    };
    
  } // Reduction::
}// DANSE::

#endif// REDUCTION_REBINTOF2E_H

// version
// $Id$

// End of file 
