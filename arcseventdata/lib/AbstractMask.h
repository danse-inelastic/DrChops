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


#ifndef H_ARCS_EVENTDATA_ABSTRACTMASK
#define H_ARCS_EVENTDATA_ABSTRACTMASK


#include "histogram/EvenlySpacedGridData_2D.h"

namespace ARCS_EventData{

  class AbstractMask {
  public:

    // types
    typedef unsigned int index_t;

    // meta methods
    ~AbstractMask() {}

    // metods
    virtual bool operator() ( index_t pixelID ) const = 0;
  };

  class NoMask: public AbstractMask {
  public:

    // methods
    virtual bool operator() ( index_t pixelID ) const {
      return 0;
    }
  };

}// ARCS_EventData

#endif 


// version
// $Id$

// End of file 
