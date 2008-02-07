#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/events2Ix.h"
#include "arcseventdata/Ipix.h"
#include "arcseventdata/EventsReader.h"
#include "arcseventdata/ioutils.h"


int run( const char *filename,  size_t Nevents, 
	 unsigned int pixelIDbegin, unsigned int pixelIDend, unsigned int pixelIDstep,
	 const char *outfilename)
{

  using namespace ARCS_EventData;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  Ipix ipix( pixelIDbegin, pixelIDend, pixelIDstep );
  ipix.clear();
  
  events2Ix< Event2pixelID, Ipix > (pevents, Nevents, e2pixelID, ipix);

  unsigned int * intensities = ipix.intensities;
  
  delete [] pevents;

  // save histogram to a 2col ascii
  dumpIx<unsigned int, unsigned int>( ipix, outfilename );

  delete [] intensities;

  return 0;
}

void help()
{
  std::cout << "ipix event-data-filename Nevents pixelIDbegin pixelIDend pixelIDstep output-filename" << std::endl;
}


int main( int argc, char ** argv )
{
  if (argc != 7 ) { help(); exit(1); }

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int pixelIDbegin = atoi( argv[3] );
  unsigned int pixelIDend = atoi( argv[4] );
  unsigned int pixelIDstep = atoi( argv[5] );

  char *ofilename = argv[6];

  run( filename, Nevents, pixelIDbegin, pixelIDend, pixelIDstep, ofilename );

  return 0;
}



