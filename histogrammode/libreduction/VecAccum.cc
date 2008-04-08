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



#include "VecAccum.h"
#include <string>
#include <iostream>

namespace DANSE {
  namespace Reduction {
    
    template <typename NumT>
    void VecAccum<NumT>::operator()( std::vector<NumT> const & source,
                                     std::slice const & srcSlice,
                                     std::slice const & targSlice)
    {
      if (srcSlice.size() != targSlice.size())
	throw std::string("VecAccum<NumT>::operator() mismatched slices");
      
      size_t targIdx = targSlice.start();
      size_t srcIdx = srcSlice.start();
      size_t targStride = targSlice.stride();
      size_t srcStride = srcSlice.stride();
      
      for(size_t i=0; i<targSlice.size(); ++i)
        {
	  m_target[targIdx] += source[srcIdx];
	  targIdx += targStride;
	  srcIdx += srcStride;
        }
      return;
    }
    
    template <typename NumT>
    void VecAccum<NumT>::operator()( std::vector<NumT> const & source,
                                     std::slice const & targSlice)
    {
      if (source.size() != targSlice.size())
	throw std::string("VecAccum<NumT>::operator() mismatched slices");
      size_t targIdx = targSlice.start();
      size_t srcIdx = 0;
      size_t targStride = targSlice.stride();
      
      for(size_t i=0; i<targSlice.size(); ++i)
        {
	  m_target[targIdx] += source[srcIdx];
	  targIdx += targStride;
	  srcIdx++;
        }
      return;
    }
    
    template <typename NumT>
    VecAccum<NumT>::VecAccum( std::vector<NumT> & target)
      : m_target( target)
    {;}
    
    // explicit instantiations
    template class VecAccum<double>;
    template class VecAccum<float>;
    template class VecAccum<int>;
    template class VecAccum<unsigned int>;
    
  } // Reduction::
} // DANSE::

// version
// $Id: VecAccum.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
