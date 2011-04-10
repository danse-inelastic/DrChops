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

#include <cassert>
#include <fstream>
#include <iostream>

#ifdef DEBUG
#include "journal/debug.h"
#endif

#include "_macros.h"


DRCHOPS_NAMESPACE_START

namespace readPixelPositions_Impl {
  const char jrnltag[] = "readPixelPositions";
}
  
double *readPixelPositions
( const char * infilename, 
  int npacks = 115,
  int ndetsperpack = 8,
  int npixelsperdet = 128)
{
  using namespace std;
  ifstream is( infilename, ios::binary ); 
  if (! is.good() ) {
    std::cerr << "unable to open file" << infilename << std::endl;
    return NULL;
  }
    
  // get length of file:
  is.seekg (0, ios::end);
  size_t length; length = is.tellg();
  is.seekg (0, ios::beg);
    
  //check
  static const int nbytesperdouble=8, ndoublepervector=3;
  assert(length==(npacks)*ndetsperpack*npixelsperdet*ndoublepervector*nbytesperdouble);
    
  // read
  char *buffer = new char[length];
  is.read( buffer, length );
  is.close();
    
  double * ret =  (double *) buffer;
#ifdef DEBUG
  journal::debug_t debug( readPixelPositions_Impl::jrnltag );
  debug << journal::at(__HERE__)
	<< "readPixelPositions: buffer = " << ret 
	<< journal::endl;
#endif
  return ret;
}
  
DRCHOPS_NAMESPACE_END


// version
// $Id$

// End of file 
