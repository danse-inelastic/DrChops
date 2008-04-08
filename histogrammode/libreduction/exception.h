// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2005 All Rights Reserved  
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//

#ifndef DANSE_REDUCTION_EXCEPTION_H
#define DANSE_REDUCTION_EXCEPTION_H


#ifndef STRING_INCLUDED
#define STRING_INCLUDED
#include <string>
#endif

#ifndef EXCEPTION_INCLUDED
#define EXCEPTION_INCLUDED
#include <exception>
#endif

#ifndef JOURNAL_ERROR_H_INCLUDED
#define JOURNAL_ERROR_H_INCLUDED
#include "journal/error.h"
#endif


namespace DANSE{ 
  namespace Reduction{
    
    
    /// Exception base class for DANSE::Reduction codes
    
    class Exception: public std::exception{
      
    public:
      
      Exception(const char *m) {_msg = std::string(m);}
      const char *what() const throw()  { return _msg.c_str(); }
      ~Exception() throw() {}
      
    private:
      std::string _msg;
      
    };
    
    
    /// throw an exception and print out error message through journal
    /*!
      @param channel:  journal channel name
      @param where: usually journal::at(__HERE__)
      @param e: exception instance
    */
    template <typename loc_t>
    void throw_( const char *channel, const loc_t &where, const DANSE::Reduction::Exception &e)
    {
      journal::error_t err(channel);
      err << where
	  << e.what()
	  << journal::endl;
      throw e;
    }
    
    
    /// throw an exception and print out error message through journal
    /*!
      the type of exception to throw is given as template parameter
      @param channel: journal channel name
      @param where: usually journal::at(__HERE__)
    */
    template <typename exception_t, typename loc_t>
    void throw_( const char *channel, const loc_t &where)
    {
      journal::error_t err(channel);
      exception_t e;
      err << where
	  << e.what()
	  << journal::endl;
      throw e;
    }
    
    
    //   void throw_( const char *channel, const journal::loc3_t & whre, const Exception & e );
    //   void throw_( const char *channel, const journal::loc2_t & whre, const Exception & e );
  } // Reduction::
} //DANSE::

#endif //DANSE_REDUCTION_EXCEPTION_H


// version
// $Id$

// End of file 
