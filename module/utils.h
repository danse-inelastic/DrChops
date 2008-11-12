// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                             Tim Kelley, Jiao Lin
//                      California Institute of Technology
//                      (C) 2004-2008  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


// should this be moved into binding directory ?


#ifndef DANSE_REDUCTION_UTILS_H
#define DANSE_REDUCTION_UTILS_H

#ifndef PYTHON_INCLUDED
#define PYTHON_INCLUDED
#include "Python.h"
#endif


namespace DANSE {

  namespace Reduction {
    
    namespace utils {

      // general dtor      
      template <typename T> void deleteHeapObj( void *ptr);
      
    } // utils::
    
  } // reduction::

} // DANSE::


// include template function definitions (no instantiations!)
#define DANSE_REDUCTION_UTILS_ICC
#include "utils.icc"
#undef DANSE_REDUCTION_UTILS_ICC


#endif  // DANSE_REDUCTION_UTILS_H


// version
// $Id: utils.h 1431 2007-11-03 20:36:41Z linjiao $

// End of file
