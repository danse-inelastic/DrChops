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


#include <math.h>
#include <iostream>
#include <cassert>

#include "abs.h"
#include "physics.h"



namespace DANSE{
  namespace Physics{
    
    namespace Statistics{
      
      //! Bose Einstein Distribution
      /*!
	\param energy energy in (meV)
	\param temperature temperature in (Kelvin)
      */
      double BoseEinsteinDistribution(double energy, double temperature)
      {
	const double &T2E = Physics::Units::Conversion::Kelvin2meV;
	if (energy <0 ) {
	  std::cerr << "Warning: in file " <<__FILE__<<" line"<<__LINE__<<","
		    << "energy = " << energy 
		    << std::endl;
	  energy = std::abs(energy);
	}
	//assert( energy > 0 );
	/*
	  std::cout << "In file "<<__FILE__<<", line " << __LINE__<<", "
	  << "energy = " << energy
	  << "temperature = " << temperature 
	  << std::endl;
	*/
	return 1/(exp(energy/(temperature*T2E))-1);
      }
    }
    
  }
}


// version
// $Id$

// End of file
