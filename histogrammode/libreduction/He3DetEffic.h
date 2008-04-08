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


#ifndef DANSE_REDUCTION_HE3DETEFFIC_H
#define DANSE_REDUCTION_HE3DETEFFIC_H

#include "journal/debug.h"

namespace DANSE {
  namespace Reduction {
    
    /*! \brief He3 detector efficiencey calculator
     *
     *  Compute He3 detector tube efficiency given pressure, radius, and neutron energy.
     *
     *  Detector tube is assumed to be a cylinder. Pressure is assumed to be steady
     *  and uniform. Several () operators are defined, but they are
     *  just different versions of similar functionality: compute detector
     *  efficiency given the neutron energy(ies).
     *
     *  The algorithm is a straighforward integration. Neutron could pass
     *  a detector at various paths, but this problem becomes a simple one
     *  with an assumption: all neutrons run through the tube in perpendicular
     *  to the axis of the tube.
     *  Therefore, the only integration variable is the distance from
     *  tube center axis to the neutron trace.
     *
     *  Template parameters:
     *  \param FPT floating point type
     *  \param EnergyIterator iterator type for energy array
     *  \param EfficiencyIterator iterator type for efficiency array
     */
    template  <typename FPT, 
	       typename EnergyIterator = FPT*, 
	       typename EfficiencyIterator = EnergyIterator>
    class He3DetEffic
    {
    public: 
      
      // interface
      
      /*! \brief Compute detector efficiency for He3 detector 
       *  at the energy supplied. 
       * 
       * \param energy neutron energy
       */
      FPT operator()( FPT energy);
      
      /*! \brief Compute detector efficiency for He3 detector
       *  at the energies supplied
       *
       * Iterator version. Assume energy and efficiency containers same
       * size. 
       * effEnd should be one-past-the-end of the efficiency 
       * container. 
       *
       * efficiencies must be all zeros!
       *
       * \param energyStart start iterator of energy array 
       * \param effStart start iterator of output efficiency array
       * \param effEnd end iterator of output efficiency array
       */
      void operator()( const EnergyIterator energyStart,
		       EfficiencyIterator effStart, EfficiencyIterator effEnd) const;
      
      
      // meta
      
      /*! \brief ctor
       *
       * \param radius Radius of tube. Tube is assumed to be a cylinder. Units: cm
       * \param pressure Pressure of He3 in detector tube. Units: Atmospheres
       * \param npts Number of points per side of grid used for integration
       */
      explicit He3DetEffic( FPT pressure, FPT radius = 1.27, 
			    unsigned npts = 500)
	: m_pressure( pressure), 
	  m_radius( radius),
	  m_refAbsXS( 5333.0e-24/1.798),
	  m_refWavelength( 1.798),
	  m_N( pressure*1.468e20/6.0),
	  m_npts( npts)
      {
#ifdef DEBUG
	journal::debug_t debug("He3DetEffic");
	debug << journal::at(__HERE__)
	      << "ctor: pressure " << pressure 
	      << ", radius " << radius
	      << ", npts " << npts
	      << journal::endl;
#endif
      }
      
      
      // state
    private:
      
      FPT m_pressure;
      FPT m_radius;
      
      /*! Absorption x-section of He3 in cm^2 at ref. wavelength (actual
       *  number stored is divided by ref wavelength for convenience)
       */
      FPT m_refAbsXS;
      FPT m_refWavelength;
      
      /*! Number density of He3. Computed from pressure
       */
      FPT m_N;
      
      /*! Number of points per side of grid
       */
      unsigned m_npts;
      
    };  // class He3DetEffic<T>
    
  } // Reduction::
} // DANSE::


#define DANSE_REDUCTION_HE3DETEFFIC_ICC
#include "He3DetEffic.icc"
#undef DANSE_REDUCTION_HE3DETEFFIC_ICC


#endif // DANSE_REDUCTION_HE3DETEFFIC_H

// version
// $Id: He3DetEffic.h 1444 2007-11-16 16:46:15Z linjiao $

// End of file
