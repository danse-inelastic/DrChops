// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2004-2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#ifndef DANSE_REDUCTION_QBINCALCOR_H
#define DANSE_REDUCTION_QBINCALCOR_H



#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif


namespace DANSE {
  namespace Reduction {
    
    template <typename NumT>
    class QBinCalcor
    {
    public:
      /// operator(): given a set of phi bins and an incident energy,
      /// compute the corresponding scalar-Q bin boundaries for a 
      /// fixed final energy.
      void operator()( NumT finalEnergy,
		       std::vector<NumT> &QBinBounds) const;
      /// ctor: phiBinBoundaries (in degrees or radians), incident energy
      /// if boundaries given in radians, be sure to specify true in the
      /// third argument.
      QBinCalcor( std::vector<NumT> const & phiBB, 
		  NumT incidentEnergy,
		  bool inRadians = false);

    private:
      std::vector< NumT> m_cosPhi;
      NumT m_ei, m_ki2, m_ki;
      void _convertToCosPhi( std::vector<NumT> const &, bool);
      NumT _toQ ( NumT kf, NumT cosPhi) const { 
	return sqrt( m_ki2 + kf*kf - 2.0*m_ki*kf*cosPhi);}
      /// What you multiply times E to get k squared:
      static NumT e_to_k2;
    };
    
  } // Reduction::
} // DANSE::

#endif // DANSE_REDUCTION_QBINCALCOR_H



// version
// $Id: QBinCalcor.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
