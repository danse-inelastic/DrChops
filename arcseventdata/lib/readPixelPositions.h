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


#ifndef H_ARCSEVENTDATA_READPIXELPOSITIONS
#define H_ARCSEVENTDATA_READPIXELPOSITIONS

namespace ARCS_EventData{
  
  
  double *readPixelPositions( const char * infilename, int npacks = 115, int ndetsperpack = 8,
			      int npixelsperdet = 128);
  
}

#endif // H_ARCSEVENTDATA_READPIXELPOSITIONS


// version
// $Id$

// End of file 
