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


#include <iostream>
#include <cassert>

#include "EventsReader.h"
#ifdef DEBUG
#include "journal/debug.h"
#endif
#include "journal/warning.h"


namespace EventsReader_Impl {
  const char jrnltag[] = "EventsReader";
}


size_t getsize( std::ifstream & is )
{
  is.seekg(0, std::ios::end);
  size_t len = is.tellg();
  is.seekg(0, std::ios::beg);
  return len;
}



ARCS_EventData::EventsReader::EventsReader( const char * filename ) 
  : m_f( new std::ifstream(filename, std::ios_base::binary) )
{
  if (!m_f->good()) 
    std::cerr <<  "unable to open file" << filename << std::endl;
  
  m_f->seekg(0, std::ios::beg); 
}


ARCS_EventData::EventsReader::~EventsReader() 
{ delete m_f; }


ARCS_EventData::Event *
ARCS_EventData::EventsReader::read( size_t n1, size_t n2 ) {

  //Event *events = new Event[ n ];
  assert (n1 < n2);
  size_t eventsize = sizeof(Event);
  
  size_t ntotneutrons = getsize( *m_f )/eventsize;

  if (n1 > ntotneutrons || n2 > ntotneutrons) {
    std::cerr << "Total number of neutrons: " << ntotneutrons << ", "
	      << "but you are requesting neutrons up to " << n2 <<"."
	      << std::endl;
    char * msg =  "Request number of events exceed available events";
    throw std::exception();
  }

  //std::cout << m_f << std::endl;
  //std::cout << m_f->good() << std::endl;
  //std::cout << m_f->rdstate() << std::endl;
  //std::cout << std::ios::failbit << std::endl;

  m_f->seekg( n1*sizeof(Event), std::ios::beg );

  if (!m_f->good()) {
    std::cerr << "Error to seek to the " << n1 << "th neutron" << std::endl;
    return NULL;
  }
  
  size_t n = n2-n1;

  size_t N = n*sizeof(Event);
  
  char *buffer = new char [ N ];
  
  m_f->read( buffer, N );
  
  //for (int i=0; i<N; i++) std::cout << int(buffer[i]) << std::endl ;
  
  Event *ret = (Event *)buffer;
  
#ifdef DEBUG
  journal::debug_t debug( EventsReader_Impl::jrnltag );
  debug << journal::at(__HERE__)
	<< "EventsReader: events pointer = " << ret
	<< journal::endl;
#endif
  return ret;
}


ARCS_EventData::Event *
ARCS_EventData::EventsReader::read( size_t n ) 
{
  return read( 0, n );
}


// version
// $Id$

// End of file 
