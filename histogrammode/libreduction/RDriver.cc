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


#include "RDriver.h"
#include <iostream>


#ifdef DEBUG
#include "journal/debug.h"
#endif


#ifdef DEBUG
char * jrnlTag = "RDriver";
#endif


namespace DANSE {
  namespace Reduction {
    
    template <typename NumT>
    void RDriver<NumT>::ring( std::vector<NumT> const & source,
                              NumT scatteringAngle)
    {
      std::slice speSlice;
      try
        {
	  speSlice = m_speSlicer( scatteringAngle);
	  size_t bin = m_speSlicer.phiToOffset(  scatteringAngle);
#ifdef DEBUG
	  journal::debug_t debug( jrnlTag );
	  debug << "scattering angle: " << scatteringAngle << ", "
		<< "bin: " << bin << journal::endl;
#endif
	  m_norms[bin] += 1;
	  m_accum( source, speSlice);
        }
      catch (std::string &msg)
        {
	  //            std::cerr<<"RDriver<NumT>::ring() caught: "<<msg;
	  char *lt = "PhiToSlice<Numt>::phiToOffset() phi < phiMin";
	  char *gt = "PhiToSlice<Numt>::phiToOffset() phi > phiMax";
	  //if ( msg == lt || msg == gt) ;
	  if (msg.find(lt)!=std::string::npos || msg.find(gt)!=std::string::npos);
	  //                std::cerr << "\nskipping pix#";
	  //                           << pix.pixelID()<<" in det#"
	  //                           << pix.detectorID()<<" at "
	  //                           << pix.scatteringAngle()<<" degrees.\n";
	  else 
            {
	      std::cerr<<" unhandled.\n";
	      throw msg;
            }
        }
      return;
    }
    
    
    template <typename NumT>
    RDriver<NumT>::RDriver( std::vector<NumT> & speHist,
                            size_t otherArrayLength,
                            std::vector<NumT> & phiBB)
      : m_accum( speHist),
	m_speSlicer( otherArrayLength, phiBB),
	m_norms( phiBB.size()-1)
    {;}
    
    template <typename NumT>
    RDriver<NumT>::~RDriver( )
    {
      
#ifdef DEBUG
      journal::debug_t debug(jrnlTag);
      debug << journal::at(__HERE__) << "RDriver::m_norms: " ;
      for (size_t i =0; i<m_norms.size(); i++) {
	debug << m_norms[i] << ", ";
      }
      debug << journal::endl;
#endif
    }
    
    
    // explicit instantiations
    template class RDriver<float>;
    template class RDriver<double>;
    
  } // Reduction::
} // DANSE::

// version
// $Id: RDriver.cc 1431 2007-11-03 20:36:41Z linjiao $

// End of file
