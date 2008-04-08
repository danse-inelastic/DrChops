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

#ifndef VECACCUM_H
#define VECACCUM_H

#ifndef VECTOR_INCLUDED
#define VECTOR_INCLUDED
#include <vector>
#endif

// valarray included for std::slice
#ifndef VALARRAY_INCLUDED
#define VALARRAY_INCLUDED
#include <valarray>
#endif


namespace DANSE{
  namespace Reduction {
    
    template <typename NumT>
    class VecAccum
    {
    public:
      void operator()( std::vector<NumT> const & source,
		       std::slice const & srcSlice,
		       std::slice const & targSlice);
      void operator()( std::vector<NumT> const & source,
		       std::slice const & targSlice);
      explicit VecAccum( std::vector<NumT> & target);
    private: 
      std::vector<NumT> & m_target;
    };
    
  } // Reduction::
} // DANSE



#endif



// version
// $Id: VecAccum.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
