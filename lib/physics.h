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


#ifndef DANSE_REDUCTION_PHYSICS_H
#define DANSE_REDUCTION_PHYSICS_H


#include <cmath>

namespace DANSE{

  namespace Physics{
    
    const double hbar = 1.05457148e-34;
    const double atomic_mass = 1.66053886e-27;
    const double e = 1.60217653e-19;
    
    namespace Units{
      
      namespace Conversion{

	//! Temperature to Energy
	const double Kelvin2meV = (1/11.605);
	
	//! neutron wave vector k (AA^-1) to velocity (m/s)
	const double k2v = 629.719; 
	//! neutron velocity (m/s) to wave vector k (AA^-1)
	const double v2k = 1.58801E-3;
	
	const double se2v = 437.3949;  /* Convert sqrt(E)[meV] to v[m/s] */
	const double vs2e = 5.227e-6;	 /* Convert (v[m/s])**2 to E[meV] */
	const double se2k = se2v * v2k;  /* Convert sqrt(E)[meV] to k[AA^-1] */

	//! neutron energy (meV) to velocity (m/s)
	inline double E2v( double energy ) {
	  return std::sqrt(energy)*437.3949;
	}
	//! neutron velocity to energy 
	inline double v2E( double velocity) {
	  return velocity*velocity*5.227e-6;
	}
	//! square of neutron velocity to energy
	inline double vsquare2E( double vsquare) {
	  return vsquare*5.227e-6;
	}
	//! square of neutron k vector to energy
	inline double ksquare2E( double ksquare) {
	  return vsquare2E(k2v*k2v*ksquare);
	}
	//!  neutron k vector to energy
	inline double k2E( double k)
	{
	return ksquare2E(k*k);
	}
	//!  neutron energy to k
	inline double E2k( double E)
	{
	  return E2v(E)*v2k;
	}
      }
    }
    
    namespace Statistics{
      
      //! Bose Einstein Distribution
      /*!
	\param energy energy in (meV)
	\param temperature temperature in (Kelvin)
      */
      double BoseEinsteinDistribution(double energy, double temperature);
      
    } // Statistics::
    
  } // Physics::
  
} // DANSE::

#endif //DANSE_REDUCTION_PHYSICS_H



// version
// $Id$

// End of file

