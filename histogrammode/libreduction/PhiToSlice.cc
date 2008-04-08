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

#include "PhiToSlice.h"
#include "journal/debug.h"

namespace
{
    using journal::at; 
    using journal::endl;
    char journalname [] = "libreduction.RDriver";
} // anonymous::


namespace DANSE {
namespace Reduction {

    template <typename NumT>
    std::slice PhiToSlice<NumT>::operator()( NumT phi) const
    {
        // need facility to convert angle to bins
        size_t start = phiToOffset( phi);
        return std::slice( start*m_arrLen, m_arrLen, 1);
    }


    template <typename NumT>
    size_t PhiToSlice<NumT>::phiToOffset( NumT phi) const
    {
//         journal::debug_t debug( journalname);
        if (phi < m_phiMin) 
            throw std::string("PhiToSlice<Numt>::phiToOffset() phi < phiMin");
        if (phi > m_phiMax)
            throw std::string("PhiToSlice<Numt>::phiToOffset() phi > phiMax");

//         debug << at(__HERE__) << "phi = " << phi << "; phi_min = " << m_phiMin
//               << "; dphi = " << m_dphi << "; floor( (phi-phimin)/dphi = " 
//               << floor( static_cast<double>( (phi- m_phiMin)/m_dphi )) << endl;

        return static_cast<size_t>( 
            floor( static_cast<double>( (phi- m_phiMin)/m_dphi )) 
            );
    }

    template <typename NumT>
    PhiToSlice<NumT>::PhiToSlice( unsigned int arrayLength, 
                                  std::vector<NumT> const & phiBB)
        : m_arrLen( arrayLength), 
          m_dphi( phiBB[1] - phiBB[0]),
          m_phiMax( phiBB[ phiBB.size() - 1] ),
          m_phiMin( phiBB[0])
    {;}

    // explicit instantiations
    template class PhiToSlice<double>;
    template class PhiToSlice<float>;
    template class PhiToSlice<int>;
    template class PhiToSlice<unsigned int>;
    
} // Reduction::
} // DANSE::

// version
// $Id: PhiToSlice.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
