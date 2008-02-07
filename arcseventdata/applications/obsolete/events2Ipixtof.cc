#include <cstring>
#include <iostream>

#include "arcseventdata/Event.h"
#include "arcseventdata/mappers.h"
#include "arcseventdata/events2Ixy.h"
#include "arcseventdata/Ipixtof.h"
#include "arcseventdata/EventsReader.h"
#include "arcseventdata/ioutils.h"


int run( const char *filename,  size_t Nevents, 
	 unsigned int pixelIDbegin, unsigned int pixelIDend, unsigned int pixelIDstep,
	 unsigned int tofbegin, unsigned int tofend, unsigned int tofstep,
	 const char *outfilename)
{

  using namespace ARCS_EventData;

  // read events
  EventsReader reader( filename );

  Event * pevents = reader.read( Nevents );

  Ipixtofc ipixtof( pixelIDbegin, pixelIDend, pixelIDstep, 
		   tofbegin, tofend, tofstep );
  std::cout << "ipixtof shape = " 
	    <<  ipixtof.shape[0] << "," << ipixtof.shape[1] << std::endl;
  ipixtof.clear();
  
  events2Ixy< Event2pixelIDtofChannel, Ipixtofc > (pevents, Nevents, e2pt, ipixtof);

  delete [] pevents;

  // save histogram to a binary
  dumpIxy<unsigned int, unsigned int, unsigned int>( ipixtof, outfilename );

  unsigned int * intensities = ipixtof.intensities;
  delete [] intensities;

  return 0;
}

void help()
{
  std::cout << "ipixtof event-data-filename Nevents pixelIDbegin pixelIDend pixelIDstep tofbegin tofend tofstep output-filename" << std::endl;
}


int main( int argc, char ** argv )
{

  if (argc != 10 ) { help(); exit(1); }

  char *filename = argv[1];

  size_t Nevents = atoi( argv[2] );
  
  unsigned int pixelIDbegin = atoi( argv[3] );
  unsigned int pixelIDend = atoi( argv[4] );
  unsigned int pixelIDstep = atoi( argv[5] );

  unsigned int tofbegin = atoi( argv[6] );
  unsigned int tofend = atoi( argv[7] );
  unsigned int tofstep = atoi( argv[8] );

  char *ofilename = argv[9];

  run( filename, Nevents,
       pixelIDbegin, pixelIDend, pixelIDstep,
       tofbegin, tofend, tofstep,
       ofilename );

  return 0;

}

