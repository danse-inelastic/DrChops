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


#include "QBinCalcor.h"
#include <cmath>
#include <iostream>


namespace DANSE {
  namespace Reduction {
    
    /// Squires, (1.9):
    template <typename NumT>
    NumT QBinCalcor<NumT>::e_to_k2 = 1.0/2.072;
    
    template <typename NumT>
    QBinCalcor< NumT>::QBinCalcor( std::vector<NumT> const & phiBB, 
                                   NumT ei,
                                   bool inRadians)
      : m_cosPhi( phiBB.size()), m_ei( ei), m_ki2( ei*e_to_k2),
	m_ki( sqrt(m_ki2))
    {
      _convertToCosPhi( phiBB, inRadians);
      return;
    }
    
    
    template <typename NumT>
    void QBinCalcor<NumT>::operator()( NumT e,
                                       std::vector<NumT> &qbb) const
    {
      NumT kf = sqrt(e*e_to_k2);
      if (qbb.size() != m_cosPhi.size()) qbb.resize( m_cosPhi.size());
      for(size_t i=0; i<m_cosPhi.size(); ++i)
        {
	  qbb[i] = _toQ( kf, m_cosPhi[i]);
        }
      return;
    }
    
    template <typename NumT>
    void QBinCalcor<NumT>::_convertToCosPhi( std::vector<NumT> const & phiBB,
                                             bool inRadians)
    {
      double pi_on_180 = 0.01745329251994329577;
      if (! inRadians)
        {
	  for(size_t i=0; i<m_cosPhi.size(); ++i)
            {
	      m_cosPhi[i] = cos( phiBB[i]*pi_on_180);
            }
        }
      else
        {
	  for(size_t i=0; i<m_cosPhi.size(); ++i)
            {
	      m_cosPhi[i] = cos( phiBB[i]);
            }
        }
      return;
    }
    
    // explicit instantiation
    template class QBinCalcor<double>;
    template class QBinCalcor<float>;
    
  } // Reduction::
} // DANSE::

// version
// $Id: QBinCalcor.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
