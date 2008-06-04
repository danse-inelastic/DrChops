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


#include <vector>
#include "He3DetEffic.h"

namespace DANSE {
  namespace Reduction {
    
    //explicit instantiations
    
    template class He3DetEffic<double>;
    template class He3DetEffic<float>;
    
    template class He3DetEffic<double, std::vector<double>::iterator>;
    template class He3DetEffic<float, std::vector<float>::iterator>;
    
    namespace He3DetEffic_impl{
      char * journaltag = "he3deteffic";
    }
  } // Reduction::
} // DANSE::

// version
// $Id: He3DetEffic.cc 1443 2007-11-15 07:17:37Z linjiao $

// End of file
