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


#ifndef DANSE_REDUCTION_SORT_H
#define DANSE_REDUCTION_SORT_H


#include "exception.h"


namespace DANSE{
  
  namespace Reduction {
    
    class SmallArrayError: public Exception {
      
    public:
      SmallArrayError( const char * msg = "Array size must be larger than 1" ) 
	: Exception( msg ) {}
    };
    
    class OutOfBoundError: public Exception {
    public:
      OutOfBoundError( const char * msg = "Out of bound" )
	: Exception( msg ) {}
    };
    
    /// find index of the cell  [a[i], a[i+1]) that contains the given
    /// value. 
    /// assumption: a is ascending.
    template< typename InputIterator, typename FLT>
    size_t findCellIndex( FLT value, InputIterator begin, InputIterator end )
    {
      if (end-begin < 2 ) throw SmallArrayError();
      if (value< *begin or value > *(end-1)) throw OutOfBoundError();
      if (*(end-1) < *begin) throw Exception( "array must be ascending" );
      
      size_t n = end-begin;
      
      size_t i=0, j = n/2, k = n-1;
      
      while (i!=j and j!=k) {
	const FLT & middle = *(begin+j);
	if (middle < value) { i = j; j = (i+k)/2; }
	else if (value < middle) { k = j; j = (i+k)/2; }
	else return j;
      }
      
      if (i==j) return i;
      return j;
    }
    
  } // namespace Reduction
  
} // namespace DANSE


#endif // DANSE_REDUCTION_SORT_H


// version
// $Id$

// End of file 
