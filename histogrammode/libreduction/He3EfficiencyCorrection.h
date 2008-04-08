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


#ifndef REDUCTION_HE3EFFICIENCYCORRECTION_H
#define REDUCTION_HE3EFFICIENCYCORRECTION_H

#include <vector>
#include <utility>
#include <map>
#include "journal/debug.h"
#include "journal/error.h"
#include "He3DetEffic.h"

namespace DANSE { namespace Reduction{

    namespace He3EfficiencyCorrection_impl{
      extern const char * jrnltag;
    }

    /// apply efficiency correction.
    /// Given He3 tube pressure and radius, 
    /// correct intensity (as a function of neutron energy)
    /// by absorption efficiency of He3 tube
    template <typename DataType, 
	      typename EnergyIteratorType, 
	      typename IntensityIteratorType = EnergyIteratorType>
    class He3EfficiencyCorrection {
      
    public:
      /// ctor.
      /// Ebegin: begin iterator of energy array
      /// Eend: end iterator of energy array
      He3EfficiencyCorrection( const EnergyIteratorType Ebegin, 
			       const EnergyIteratorType Eend )
	:m_epsilon( 1.e-5 ),
	 m_Ebegin( Ebegin ),
	 m_Eend( Eend ),
	 m_nEnergies( Eend-Ebegin )
      {
	if (m_nEnergies<=0 ) {
	  using namespace He3EfficiencyCorrection_impl;
	  journal::error_t err(jrnltag);
	  err << "# of Energy bins must be positive: " << m_nEnergies << journal::endl;
	  throw;
	}
      }

      /// correct  intensities of a pixel given its pressure and radius
      /// intensities: array of intensities I(E) for the pixel
      /// pressure: pressure of a pixel (atm)
      /// radius: radius of a pixel (cm)
      void correct( IntensityIteratorType intensities,
		    const DataType & pressure, const DataType & radius) 
      {
	EfficArray effs = _getEfficiency( PressureRadiusPair( pressure, radius ) );
	for (size_t i=0; i<m_nEnergies; i++)
	  *(intensities+i) /= effs[i];
      }
      
    private:
      const DataType m_epsilon;
      const EnergyIteratorType m_Ebegin, m_Eend; 
      size_t m_nEnergies;
      typedef std::pair<DataType, DataType> PressureRadiusPair; // pressure, radius pair
      typedef std::vector<DataType> EfficArray; // efficiency array

      typedef PressureRadiusPair Key;
      typedef EfficArray Value;
      bool _equal( const Key & key1, const Key & key2 ) const 
      {
	if (&key1 == &key2) return 1;
	if (key1.first == key2.first && key1.second == key2.second) return 1;
	if (key1.first<=0 || key2.first<=0) {
	  using namespace He3EfficiencyCorrection_impl;
	  journal::error_t err(jrnltag);
	  err << "pressure must all be positive: "
	      << key1.first
	      << ", " << key2.first
	      << journal::endl ;
	  throw;
	}
	if (key1.second<=0 || key2.second<=0) {
	  using namespace He3EfficiencyCorrection_impl;
	  journal::error_t err(jrnltag);
	  err << "radius must all be positive: "
	      << key1.second
	      << ", " << key2.second;
	  throw;
	}
	if (std::abs((key1.first-key2.first)/key1.first) < m_epsilon
	    && std::abs((key1.second-key2.second)/key1.second) < m_epsilon )
	  return 1;
	return 0;
      }

      struct ltkey
      {
	bool operator()(const Key& k1, const Key& k2) const
	{
	  return k1.first < k2.first;
	}
      };
      std::map<Key, Value, ltkey> m_cache;

      EfficArray _getEfficiency( const PressureRadiusPair & pr )
      {
	EfficArray ret = m_cache[ pr ];
	
	if (ret.size()==0) 
	  ret = m_cache[ pr ] = _calculate( pr );
	
	return ret;
      }

      EfficArray _calculate( const PressureRadiusPair & pr ) const
      {
	He3DetEffic<DataType, EnergyIteratorType, typename EfficArray::iterator>
	  calcor( pr.first, pr.second );
	EfficArray result( m_nEnergies );
	calcor( m_Ebegin, result.begin(), result.end() );
#ifdef DEBUG
	using namespace He3EfficiencyCorrection_impl;
	journal::debug_t debug( jrnltag );
	debug << journal::at(__HERE__) 
	      << "detector efficiency:" ;
	for (size_t i=0; i<result.size(); i++) {
	  debug << result[i] << ", ";
	}
	debug << journal::endl;
#endif
	return result;
      }
      
    }; // He3EfficiencyCorrection:


}}//namespace DANSE::Reduction



#endif// REDUCTION_HE3EFFICIENCYCORRECTION_H

// version
// $Id$

// End of file 
