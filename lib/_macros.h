// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                      (C) 2006-2011  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef DRCHOPS__MACROS_H
#define DRCHOPS__MACROS_H


#ifdef USE_DANSE_NAMESPACE
#define DRCHOPS_NAMESPACE_START namespace DANSE {namespace reduction{
#define DRCHOPS_NAMESPACE_END }}
#define USING_DRCHOPS_NAMESPACE using namespace DANSE::reduction;
#else
#define DRCHOPS_NAMESPACE_START namespace drchops{
#define DRCHOPS_NAMESPACE_END }
#define USING_DRCHOPS_NAMESPACE using namespace drchops;
#endif


#endif


// version
// $Id$

// End of file 
  
