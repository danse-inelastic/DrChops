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


#ifndef DRCHOPS_READPIXELPOSITIONS_H
#define DRCHOPS_READPIXELPOSITIONS_H


#include "_macros.h"

DRCHOPS_NAMESPACE_START
    
double *readPixelPositions
( const char * infilename, int npacks = 115, int ndetsperpack = 8,
  int npixelsperdet = 128);

DRCHOPS_NAMESPACE_END

#endif // DRCHOPS_READPIXELPOSITIONS_H


// version
// $Id$

// End of file 
