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


#ifndef DANSE_REDUCTION_FUNCTOR_H
#define DANSE_REDUCTION_FUNCTOR_H


namespace DANSE{  
  namespace Reduction
  {
    
    /// abstract base class of functor
    template <typename InputType, typename OutputType>
    class Functor{
      
    public:
      virtual OutputType operator() ( const InputType & ) = 0;
      virtual ~Functor() {};
    };
    
  } // Reduction::
} // DANSE::


#endif // DANSE_REDUCTION_FUNCTOR_H


// version
// $Id: ERebinAllInOne.h 522 2005-07-11 18:45:08Z tim $

// End of file
