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


#ifndef H_ARCS_EVENTDATA_IOUTILS
#define H_ARCS_EVENTDATA_IOUTILS

#include "histogram/EvenlySpacedGridData_1D.h"
#include "histogram/EvenlySpacedGridData_2D.h"

namespace ARCS_EventData{

  using DANSE::Histogram::EvenlySpacedGridData_1D;

  template <typename XDatatype, typename IDatatype>
  void dumpIx( const EvenlySpacedGridData_1D< XDatatype, IDatatype > & ix, 
	       const char * filename )
  {
    std::ofstream of( filename );

    for (unsigned int i=0; i<ix.size; i++) 
      of << ix.xbegin + i * ix.xstep + ix.xstep/2 
	 << "\t" << *(ix.yarray + i)
	 << std::endl;

    of.close();
    
    return;
  }


  using DANSE::Histogram::EvenlySpacedGridData_2D;

  /// dump Ixy to a binary data file.
  /// This is not really a structured way to save data. 
  /// The purpose for now is that we will be able to save this
  /// histogram to a binary data file, and then read it
  /// from python and save the histogram in hdf5 file format.
  /// This way, we don't need to write python bindings of
  /// all these codes. 
  /// Future, we should have python bindings for this c++ library,
  /// and we will not need this function.
  template <typename XDatatype, typename YDatatype, typename IDatatype>
  void dumpIxy
  ( const EvenlySpacedGridData_2D< XDatatype, YDatatype, IDatatype > & ixy, 
    const char * filename )
  {
    std::ofstream of( filename, std::ios::binary );
    XDatatype x; YDatatype y;
    
    std::cout << "In dumpIxy" << std::endl;
    std::cout << "ixy shape: " << ixy.shape[0] << "," << ixy.shape[1] << std::endl;

    char * buf = (char *) ixy.intensities; // bad implementation. intensities could be any iterator, but here we assume that intensities is a pointer
    size_t n = ixy.size * sizeof( IDatatype ) ;
    of.write(buf, n );

    std::cout << n << " data written" << std::endl;
    of.close();
    
    return;
  }

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
